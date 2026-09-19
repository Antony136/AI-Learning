from app.ingestion.pipeline import ingest_pdf


PDF_PATH = "documents/genai-notes.pdf"


if __name__ == "__main__":
    ingest_pdf(PDF_PATH)