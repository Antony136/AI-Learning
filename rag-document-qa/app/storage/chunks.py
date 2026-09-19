from app.core.database import get_connection


def create_document(filename: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (filename)
                VALUES (%s)
                RETURNING id
                """,
                (filename,)
            )

            document_id = cursor.fetchone()[0]

        connection.commit()

        return document_id

    finally:
        connection.close()


def insert_chunk(
    document_id: int,
    source: str,
    page: int,
    chunk_index: int,
    content: str,
    embedding: list[float]
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO document_chunks
                (
                    document_id,
                    source,
                    page,
                    chunk_index,
                    content,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    document_id,
                    source,
                    page,
                    chunk_index,
                    content,
                    embedding
                )
            )

        connection.commit()

    finally:
        connection.close()


def clear_chunks():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM document_chunks"
            )

        connection.commit()

    finally:
        connection.close()