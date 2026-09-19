from app.core.database import get_connection


def insert_chunk(
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
                (source, page, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
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