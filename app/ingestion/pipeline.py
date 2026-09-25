from pathlib import Path

from app.ingestion.extract import extract_pages
from app.ingestion.chunker import chunk_text
from app.ingestion.embeddings import generate_embedding
from app.storage.chunks import (
    create_document,
    insert_chunk,
    update_document_metadata
)


def ingest_document(
    pdf_path: str,
    on_progress=None,
    chunk_size: int = 1000,
    overlap_sentences: int = 1
):
    pdf_file = Path(pdf_path)

    file_size = pdf_file.stat().st_size

    document_id = create_document(
        filename=pdf_file.name,
        file_size=file_size,
        file_path=str(pdf_file)
    )

    try:

        # ---------------------------------------------------------
        # Stage 1: Extract text
        # ---------------------------------------------------------

        if on_progress:
            on_progress(
                "extracting",
                0,
                0
            )

        pages = extract_pages(
            pdf_path
        )


        if on_progress:
            on_progress(
                "extracting",
                len(pages),
                len(pages)
            )


        # ---------------------------------------------------------
        # Stage 2: Create chunks
        # ---------------------------------------------------------

        if on_progress:
            on_progress(
                "chunking",
                0,
                len(pages)
            )

        page_chunks = []
        total_chunks = 0

        for page_index, page_data in enumerate(
            pages,
            start=1
        ):

            page_number = page_data["page"]
            page_text = page_data["text"]

            chunks = chunk_text(
                page_text,
                chunk_size=chunk_size,
                overlap_sentences=overlap_sentences
            )

            page_chunks.append(
                (page_number, chunks)
            )

            total_chunks += len(chunks)


            if on_progress:
                on_progress(
                    "chunking",
                    page_index,
                    len(pages)
                )


        # ---------------------------------------------------------
        # Stage 3: Generate embeddings
        # ---------------------------------------------------------

        if on_progress:
            on_progress(
                "embedding",
                0,
                total_chunks
            )

        embedded_chunks = []

        completed_embeddings = 0

        for page_number, chunks in page_chunks:

            for chunk_index, chunk in enumerate(
                chunks,
                start=1
            ):

                embedding = generate_embedding(
                    chunk
                )

                embedded_chunks.append({
                    "page": page_number,
                    "chunk_index": chunk_index,
                    "content": chunk,
                    "embedding": embedding
                })

                completed_embeddings += 1


                if on_progress:
                    on_progress(
                        "embedding",
                        completed_embeddings,
                        total_chunks
                    )


        # ---------------------------------------------------------
        # Stage 4: Store chunks
        # ---------------------------------------------------------

        if on_progress:
            on_progress(
                "storing",
                0,
                total_chunks
            )

        completed_storage = 0

        for chunk in embedded_chunks:

            insert_chunk(
                document_id=document_id,
                source=pdf_file.name,
                page=chunk["page"],
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                embedding=chunk["embedding"]
            )

            completed_storage += 1


            if on_progress:
                on_progress(
                    "storing",
                    completed_storage,
                    total_chunks
                )


        # ---------------------------------------------------------
        # Stage 5: Complete
        # ---------------------------------------------------------

        update_document_metadata(
            document_id=document_id,
            page_count=len(pages),
            chunk_count=total_chunks,
            status="ready",
            stage="ready"
        )


        if on_progress:
            on_progress(
                "ready",
                total_chunks,
                total_chunks
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

        update_document_metadata(
            document_id=document_id,
            page_count=0,
            chunk_count=0,
            status="failed",
            stage="failed"
        )

        if on_progress:
            on_progress(
                "failed",
                0,
                0
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