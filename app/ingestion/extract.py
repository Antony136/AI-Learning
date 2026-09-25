import html
import re

from pypdf import PdfReader


def _normalize_whitespace(text: str) -> str:
    """
    Normalize spaces and tabs while preserving meaningful newlines.
    """

    text = html.unescape(text)

    # Normalize non-breaking spaces and similar whitespace.
    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", "")
    text = text.replace("\ufeff", "")

    # Remove trailing whitespace.
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Collapse repeated spaces/tabs.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", text)

    return text.strip()


def _join_broken_lines(text: str) -> str:
    """
    Join lines that were broken by PDF extraction but belong
    to the same paragraph.

    Important:
    - Paragraph boundaries are preserved.
    - Bullet/numbered/list lines are preserved.
    - Headings are preserved.
    """

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            cleaned_lines.append("")
            continue

        cleaned_lines.append(line)

    result = []

    for line in cleaned_lines:
        if not result:
            result.append(line)
            continue

        previous = result[-1]

        # Preserve blank lines.
        if not previous:
            result.append(line)
            continue

        # Preserve list items.
        if _is_list_item(line):
            result.append(line)
            continue

        # Preserve likely headings.
        if _is_heading(line):
            result.append(line)
            continue

        # If previous line already looks like a heading/list,
        # don't blindly merge with the next line.
        if _is_heading(previous) or _is_list_item(previous):
            result.append(line)
            continue

        # Join normal PDF line wrapping.
        #
        # Example:
        #
        # "Professional ethics requires engineers to give importance"
        # "to public safety and welfare."
        #
        # becomes:
        #
        # "Professional ethics requires engineers to give importance to
        # public safety and welfare."
        if not previous.endswith((".", "!", "?", ":", ";")):
            result[-1] = f"{previous} {line}"
        else:
            result.append(line)

    return "\n".join(result)


def _is_list_item(line: str) -> bool:
    """
    Detect common numbered, lettered and bullet list formats.
    """

    patterns = [
        r"^[•●▪◦‣–—-]\s+",
        r"^\d+[.)]\s+",
        r"^[a-zA-Z][.)]\s+",
        r"^[ivxlcdmIVXLCDM]+[.)]\s+",
    ]

    return any(
        re.match(pattern, line)
        for pattern in patterns
    )


def _is_heading(line: str) -> bool:
    """
    Detect likely section headings without trying to understand
    the document semantically.
    """

    line = line.strip()

    if not line:
        return False

    # Very long lines are unlikely to be headings.
    if len(line) > 120:
        return False

    # Existing numbered headings.
    if re.match(
        r"^(?:\d+(?:\.\d+)*|[IVXLC]+)[.)]?\s+\S+",
        line,
        flags=re.IGNORECASE
    ):
        return True

    # Common heading patterns.
    heading_keywords = (
        "introduction",
        "definition",
        "definitions",
        "conclusion",
        "summary",
        "objectives",
        "objective",
        "advantages",
        "disadvantages",
        "applications",
        "examples",
        "professional codes",
        "ethical responsibilities",
        "environmental concerns",
    )

    lowered = line.lower()

    if lowered.rstrip(":") in heading_keywords:
        return True

    # Short title-like lines.
    words = line.split()

    if (
        len(words) <= 10
        and line.endswith(":")
    ):
        return True

    return False


def clean_page_text(text: str) -> str:
    """
    Clean and normalize text extracted from one PDF page.
    """

    if not text:
        return ""

    text = html.unescape(text)

    # Remove common PDF/control artifacts.
    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Normalize whitespace while keeping newlines.
    text = _normalize_whitespace(text)

    if not text:
        return ""

    # Repair line wrapping caused by PDF extraction.
    text = _join_broken_lines(text)

    # Normalize whitespace one final time.
    text = _normalize_whitespace(text)

    return text


def extract_pages(pdf_path: str):
    """
    Extract and clean text from every PDF page.

    Returns:
        [
            {
                "page": 1,
                "text": "clean page text..."
            },
            ...
        ]
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):
        raw_text = page.extract_text()

        if not raw_text:
            continue

        text = clean_page_text(raw_text)

        if not text:
            continue

        pages.append({
            "page": page_number,
            "text": text
        })

    return pages