from pathlib import Path

from app.ingestion.extract import extract_pages
from app.ingestion.chunker import chunk_text
from app.ingestion.embeddings import generate_embedding
from app.storage.chunks import (
    create_document,
    insert_chunk
)


def ingest_document(
    pdf_path: str,
    chunk_size: int = 1000,
    overlap_sentences: int = 1
):
    pdf_file = Path(pdf_path)

    # Step 1: Create document record
    document_id = create_document(
        pdf_file.name
    )

    # Step 2: Extract pages
    pages = extract_pages(pdf_path)

    total_chunks = 0

    # Step 3: Process every page
    for page_data in pages:

        page_number = page_data["page"]
        page_text = page_data["text"]

        # Step 4: Split page into chunks
        chunks = chunk_text(
            page_text,
            chunk_size=chunk_size,
            overlap_sentences=overlap_sentences
        )

        # Step 5: Process every chunk
        for chunk_index, chunk in enumerate(
            chunks,
            start=1
        ):
            # Step 6: Generate embedding
            embedding = generate_embedding(
                chunk
            )

            # Step 7: Store chunk
            insert_chunk(
                document_id=document_id,
                source=pdf_file.name,
                page=page_number,
                chunk_index=chunk_index,
                content=chunk,
                embedding=embedding
            )

            total_chunks += 1

    return {
        "document_id": document_id,
        "filename": pdf_file.name,
        "pages": len(pages),
        "chunks": total_chunks
    }


if __name__ == "__main__":

    result = ingest_document(
        "documents/genai-notes.pdf"
    )

    print("\nIngestion complete")
    print("=" * 50)

    print(
        f"Document ID: {result['document_id']}"
    )

    print(
        f"Filename: {result['filename']}"
    )

    print(
        f"Pages: {result['pages']}"
    )

    print(
        f"Chunks: {result['chunks']}"
    )