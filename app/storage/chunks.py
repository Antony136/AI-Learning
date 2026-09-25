from app.core.database import get_connection


def create_document(
    filename: str,
    file_size: int | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (
                    filename,
                    file_size,
                    status
                )
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    filename,
                    file_size,
                    "processing"
                )
            )

            document_id = cursor.fetchone()[0]

        connection.commit()

        return document_id

    finally:
        connection.close()

def update_document_metadata(
    document_id: int,
    page_count: int,
    chunk_count: int,
    status: str,
    stage: str
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE documents
                SET
                    page_count = %s,
                    chunk_count = %s,
                    status = %s,
                    stage = %s
                WHERE id = %s
                """,
                (
                    page_count,
                    chunk_count,
                    status,
                    stage,
                    document_id
                )
            )

        connection.commit()

    finally:
        connection.close()

def update_document_status(
    document_id: int,
    status: str,
    stage: str
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE documents
                SET
                    status = %s,
                    stage = %s
                WHERE id = %s
                """,
                (
                    status,
                    stage,
                    document_id
                )
            )

        connection.commit()

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