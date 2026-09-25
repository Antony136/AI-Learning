import re


# ---------------------------------------------------------
# Structure detection
# ---------------------------------------------------------


def is_list_item(line: str) -> bool:
    """
    Detect common bullet, numbered and lettered list items.
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


def is_heading(line: str) -> bool:
    """
    Detect likely headings.
    """

    line = line.strip()

    if not line:
        return False

    if len(line) > 120:
        return False

    # Numbered headings:
    #
    # 1. Introduction
    # 2.1 Ethical Issues
    # I. Overview
    #
    if re.match(
        r"^(?:\d+(?:\.\d+)*|[IVXLC]+)[.)]?\s+\S+",
        line,
        flags=re.IGNORECASE
    ):
        return True

    # Short heading ending with colon.
    if (
        len(line.split()) <= 10
        and line.endswith(":")
    ):
        return True

    # Short title-like text.
    words = line.split()

    if (
        len(words) <= 8
        and len(line) <= 80
        and not line.endswith((".", "!", "?"))
    ):
        # Avoid treating ordinary short sentences as headings.
        if not re.search(
            r"\b(is|are|was|were|has|have|can|should|must)\b",
            line,
            flags=re.IGNORECASE
        ):
            return True

    return False


# ---------------------------------------------------------
# Text normalization
# ---------------------------------------------------------


def normalize_chunk_text(text: str) -> str:
    """
    Final cleanup applied to every generated chunk.
    """

    text = text.strip()

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ---------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------


def split_into_sentences(text: str):
    """
    Split text into sentences while preserving common
    abbreviations and list items reasonably well.
    """

    text = text.strip()

    if not text:
        return []

    # Protect common abbreviations from sentence splitting.
    protected = {
        "e.g.": "E<prd>G<prd>",
        "i.e.": "I<prd>E<prd>",
        "etc.": "ETC<prd>",
        "Mr.": "MR<prd>",
        "Mrs.": "MRS<prd>",
        "Dr.": "DR<prd>",
        "Prof.": "PROF<prd>",
        "Fig.": "FIG<prd>",
        "No.": "NO<prd>",
    }

    for original, replacement in protected.items():
        text = text.replace(
            original,
            replacement
        )

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    restored = []

    for sentence in sentences:
        sentence = sentence.strip()

        for original, replacement in protected.items():
            sentence = sentence.replace(
                replacement,
                original
            )

        if sentence:
            restored.append(sentence)

    return restored


# ---------------------------------------------------------
# Paragraph / block extraction
# ---------------------------------------------------------


def split_into_blocks(text: str):
    """
    Convert cleaned page text into meaningful blocks.

    Blocks can be:
    - headings
    - paragraphs
    - bullet lists
    - numbered lists
    """

    lines = [
        line.strip()
        for line in text.splitlines()
    ]

    lines = [
        line
        for line in lines
        if line
    ]

    if not lines:
        return []

    blocks = []

    current_block = []

    def flush():
        if current_block:
            block = " ".join(current_block).strip()

            if block:
                blocks.append(block)

            current_block.clear()

    for line in lines:

        # -------------------------------------------------
        # Heading
        # -------------------------------------------------

        if is_heading(line):

            flush()

            blocks.append(line)

            continue

        # -------------------------------------------------
        # List item
        # -------------------------------------------------

        if is_list_item(line):

            flush()

            blocks.append(line)

            continue

        # -------------------------------------------------
        # Normal text
        # -------------------------------------------------

        current_block.append(line)

        # A sentence ending is a useful paragraph boundary
        # when the next line is structurally different.
        if line.endswith(
            (".", "!", "?", ":")
        ):
            continue

    flush()

    return blocks


# ---------------------------------------------------------
# Semantic grouping
# ---------------------------------------------------------


def group_blocks(
    blocks,
    chunk_size: int
):
    """
    Group related blocks into chunks while respecting the
    requested maximum size.

    Headings are kept with the following content whenever
    possible.
    """

    chunks = []

    current = []

    current_length = 0

    for index, block in enumerate(blocks):

        block = normalize_chunk_text(block)

        if not block:
            continue

        block_length = len(block)

        # -------------------------------------------------
        # Very large block
        # -------------------------------------------------

        if block_length > chunk_size:

            # Flush current chunk first.
            if current:
                chunks.append(
                    normalize_chunk_text(
                        "\n".join(current)
                    )
                )

                current = []
                current_length = 0

            # Split oversized block by sentences.
            sentence_chunks = split_large_block(
                block,
                chunk_size
            )

            chunks.extend(
                sentence_chunks
            )

            continue

        # -------------------------------------------------
        # Empty chunk
        # -------------------------------------------------

        if not current:

            current.append(block)
            current_length = block_length

            continue

        # -------------------------------------------------
        # Check whether block fits
        # -------------------------------------------------

        proposed_length = (
            current_length
            + 2
            + block_length
        )

        if proposed_length <= chunk_size:

            current.append(block)

            current_length = proposed_length

            continue

        # -------------------------------------------------
        # Doesn't fit
        # -------------------------------------------------

        chunks.append(
            normalize_chunk_text(
                "\n".join(current)
            )
        )

        current = [block]

        current_length = block_length

    # Final chunk.
    if current:

        chunks.append(
            normalize_chunk_text(
                "\n".join(current)
            )
        )

    return chunks


# ---------------------------------------------------------
# Oversized block splitting
# ---------------------------------------------------------


def split_large_block(
    text: str,
    chunk_size: int
):
    """
    Split a paragraph/list that is larger than chunk_size.

    Sentence boundaries are preferred.
    """

    sentences = split_into_sentences(text)

    if not sentences:
        return [
            text[:chunk_size]
        ]

    chunks = []

    current = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        # A single sentence is larger than the limit.
        if sentence_length > chunk_size:

            if current:
                chunks.append(
                    normalize_chunk_text(
                        " ".join(current)
                    )
                )

                current = []
                current_length = 0

            # Hard split only as a last resort.
            for start in range(
                0,
                sentence_length,
                chunk_size
            ):
                piece = sentence[
                    start:start + chunk_size
                ].strip()

                if piece:
                    chunks.append(piece)

            continue

        if (
            current
            and current_length
            + sentence_length
            + 1
            > chunk_size
        ):

            chunks.append(
                normalize_chunk_text(
                    " ".join(current)
                )
            )

            current = [sentence]

            current_length = sentence_length

        else:

            current.append(sentence)

            if current_length:
                current_length += 1

            current_length += sentence_length

    if current:

        chunks.append(
            normalize_chunk_text(
                " ".join(current)
            )
        )

    return chunks


# ---------------------------------------------------------
# Overlap
# ---------------------------------------------------------


def add_overlap(
    chunks,
    overlap_sentences: int = 1
):
    """
    Add a small amount of sentence overlap between chunks.

    This is intentionally conservative so that chunks do not
    become unnecessarily repetitive.
    """

    if (
        not chunks
        or overlap_sentences <= 0
    ):
        return chunks

    result = []

    for index, chunk in enumerate(chunks):

        if index == 0:

            result.append(chunk)

            continue

        previous_sentences = split_into_sentences(
            chunks[index - 1]
        )

        overlap = previous_sentences[
            -overlap_sentences:
        ]

        if not overlap:
            result.append(chunk)

            continue

        overlap_text = " ".join(overlap)

        # Avoid duplicating content that is already
        # present at the beginning of the chunk.
        if chunk.startswith(overlap_text):

            result.append(chunk)

        else:

            result.append(
                normalize_chunk_text(
                    f"{overlap_text} {chunk}"
                )
            )

    return result


# ---------------------------------------------------------
# Public chunking function
# ---------------------------------------------------------


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap_sentences: int = 1
):
    """
    Create structure-aware chunks from a PDF page.

    Strategy:

        page text
          ↓
        structural blocks
          ↓
        semantic grouping
          ↓
        sentence fallback for oversized blocks
          ↓
        small overlap
    """

    if not text or not text.strip():
        return []

    if chunk_size < 200:
        raise ValueError(
            "chunk_size must be at least 200 characters."
        )

    if overlap_sentences < 0:
        raise ValueError(
            "overlap_sentences cannot be negative."
        )

    # -----------------------------------------------------
    # Step 1: Normalize input
    # -----------------------------------------------------

    text = normalize_chunk_text(text)

    if not text:
        return []

    # -----------------------------------------------------
    # Step 2: Extract structural blocks
    # -----------------------------------------------------

    blocks = split_into_blocks(text)

    if not blocks:
        return []

    # -----------------------------------------------------
    # Step 3: Group blocks into chunks
    # -----------------------------------------------------

    chunks = group_blocks(
        blocks,
        chunk_size
    )

    # -----------------------------------------------------
    # Step 4: Add conservative overlap
    # -----------------------------------------------------

    chunks = add_overlap(
        chunks,
        overlap_sentences
    )

    # -----------------------------------------------------
    # Step 5: Final cleanup
    # -----------------------------------------------------

    cleaned_chunks = []

    for chunk in chunks:

        chunk = normalize_chunk_text(
            chunk
        )

        if chunk:
            cleaned_chunks.append(chunk)

    return cleaned_chunks