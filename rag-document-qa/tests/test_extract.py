from pathlib import Path

from reportlab.pdfgen import canvas

from app.ingestion.extract import extract_pages


def create_test_pdf(pdf_path: Path):
    pdf = canvas.Canvas(str(pdf_path))

    pdf.drawString(
        100,
        750,
        "RAG retrieves relevant information."
    )

    pdf.showPage()

    pdf.drawString(
        100,
        750,
        "The language model uses the retrieved context."
    )

    pdf.showPage()

    pdf.save()


def test_extract_pages_returns_list(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    pages = extract_pages(str(pdf_path))

    assert isinstance(pages, list)
    assert len(pages) == 2


def test_extract_pages_contains_page_numbers(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    pages = extract_pages(str(pdf_path))

    assert pages[0]["page"] == 1
    assert pages[1]["page"] == 2


def test_extract_pages_contains_text(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    pages = extract_pages(str(pdf_path))

    assert "RAG retrieves relevant information." in pages[0]["text"]
    assert "language model uses the retrieved context." in pages[1]["text"]