from pathlib import Path

from app.ingestion.extract import extract_pages
from app.ingestion.embeddings import generate_embedding
from experiments.chunking import chunk_text
from app.core.database import get_connection


PDF_PATH = "documents/genai-notes.pdf"


def clear_experiment_table():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM document_chunks_experiment"
            )

        connection.commit()

    finally:
        connection.close()


def insert_experiment_chunk(
    source,
    page,
    chunk_index,
    chunk_size,
    overlap_sentences,
    content,
    embedding
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO document_chunks_experiment
                (
                    source,
                    page,
                    chunk_index,
                    chunk_size,
                    overlap_sentences,
                    content,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    source,
                    page,
                    chunk_index,
                    chunk_size,
                    overlap_sentences,
                    content,
                    embedding
                )
            )

        connection.commit()

    finally:
        connection.close()


def ingest_configuration(
    chunk_size,
    overlap_sentences
):
    pdf_file = Path(PDF_PATH)

    pages = extract_pages(
        PDF_PATH
    )

    total_chunks = 0

    for page_data in pages:

        page_number = page_data["page"]
        page_text = page_data["text"]

        chunks = chunk_text(
            page_text,
            chunk_size=chunk_size,
            overlap_sentences=overlap_sentences
        )

        for chunk_index, chunk in enumerate(
            chunks,
            start=1
        ):

            embedding = generate_embedding(
                chunk
            )

            insert_experiment_chunk(
                source=pdf_file.name,
                page=page_number,
                chunk_index=chunk_index,
                chunk_size=chunk_size,
                overlap_sentences=overlap_sentences,
                content=chunk,
                embedding=embedding
            )

            total_chunks += 1

    return total_chunks


if __name__ == "__main__":

    configurations = [
        (1000, 0),
        (1000, 1),
        (1000, 2)
    ]

    clear_experiment_table()

    for chunk_size, overlap in configurations:

        print(
            f"\nTesting chunk_size={chunk_size}, "
            f"overlap={overlap}"
        )

        count = ingest_configuration(
            chunk_size,
            overlap
        )

        print(
            f"Chunks created: {count}"
        )