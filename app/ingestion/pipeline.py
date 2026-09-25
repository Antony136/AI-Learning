from pathlib import Path

from app.ingestion.extract import extract_pages
from app.ingestion.chunker import chunk_text
from app.ingestion.embeddings import generate_embedding
from app.storage.chunks import (
    create_document,
    insert_chunk,
    update_document_metadata,
    update_document_status
)


def ingest_document(
    pdf_path: str,
    chunk_size: int = 1000,
    overlap_sentences: int = 1
):
    pdf_file = Path(pdf_path)

    file_size = pdf_file.stat().st_size

    document_id = create_document(
        filename=pdf_file.name,
        file_size=file_size
    )

    try:

        # Stage 1
        update_document_status(
            document_id=document_id,
            status="processing",
            stage="extracting"
        )

        pages = extract_pages(
            pdf_path
        )

        # Stage 2
        update_document_status(
            document_id=document_id,
            status="processing",
            stage="chunking"
        )

        page_chunks = []

        total_chunks = 0

        for page_data in pages:

            page_number = page_data["page"]
            page_text = page_data["text"]

            chunks = chunk_text(
                page_text,
                chunk_size=chunk_size,
                overlap_sentences=overlap_sentences
            )

            page_chunks.append(
                (
                    page_number,
                    chunks
                )
            )

            total_chunks += len(chunks)

        # Stage 3
        update_document_status(
            document_id=document_id,
            status="processing",
            stage="embedding"
        )

        embedded_chunks = []

        for page_number, chunks in page_chunks:

            for chunk_index, chunk in enumerate(
                chunks,
                start=1
            ):

                embedding = generate_embedding(
                    chunk
                )

                embedded_chunks.append(
                    {
                        "page": page_number,
                        "chunk_index": chunk_index,
                        "content": chunk,
                        "embedding": embedding
                    }
                )

        # Stage 4
        update_document_status(
            document_id=document_id,
            status="processing",
            stage="storing"
        )

        for chunk in embedded_chunks:

            insert_chunk(
                document_id=document_id,
                source=pdf_file.name,
                page=chunk["page"],
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                embedding=chunk["embedding"]
            )

        # Stage 5
        update_document_metadata(
            document_id=document_id,
            page_count=len(pages),
            chunk_count=total_chunks,
            status="ready",
            stage="ready"
        )

        return {
            "document_id": document_id,
            "filename": pdf_file.name,
            "file_size": file_size,
            "pages": len(pages),
            "chunks": total_chunks,
            "status": "ready",
            "stage": "ready"
        }

    except Exception:

        update_document_status(
            document_id=document_id,
            status="failed",
            stage="failed"
        )

        raise

    
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
        f"File size: {result['file_size']} bytes"
    )

    print(
        f"Pages: {result['pages']}"
    )

    print(
        f"Chunks: {result['chunks']}"
    )

    print(
        f"Status: {result['status']}"
    )