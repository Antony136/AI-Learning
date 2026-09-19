from pathlib import Path

from app.ingestion.extract import extract_pages
from app.ingestion.chunker import chunk_text
from app.ingestion.embeddings import generate_embedding
from app.storage.chunks import insert_chunk


def ingest_pdf(pdf_path: str):

    pdf_file = Path(pdf_path)

    print(f"Processing: {pdf_file.name}")

    pages = extract_pages(pdf_path)

    total_chunks = 0

    for page_data in pages:

        page_number = page_data["page"]
        page_text = page_data["text"]

        chunks = chunk_text(page_text)

        print(
            f"Page {page_number}: "
            f"{len(chunks)} chunks"
        )

        for chunk_index, chunk in enumerate(
            chunks,
            start=1
        ):

            embedding = generate_embedding(chunk)

            insert_chunk(
                source=pdf_file.name,
                page=page_number,
                chunk_index=chunk_index,
                content=chunk,
                embedding=embedding
            )

            total_chunks += 1

            print(
                f"  Stored chunk {chunk_index}"
            )

    print()
    print("Ingestion complete!")
    print(f"Total chunks stored: {total_chunks}")