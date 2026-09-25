from app.core.database import get_connection


def get_documents():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    d.id,
                    d.filename,
                    d.file_size,
                    d.page_count,
                    d.chunk_count,
                    d.status,
                    d.stage,
                    d.created_at,
                    d.file_path
                FROM documents d
                ORDER BY d.created_at DESC
                """
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "filename": row[1],
                "file_size": row[2],
                "page_count": row[3],
                "chunk_count": row[4],
                "status": row[5],
                "stage": row[6],
                "created_at": row[7],
                "file_path": row[8]
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_document(document_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    d.id,
                    d.filename,
                    d.file_size,
                    d.page_count,
                    d.chunk_count,
                    d.status,
                    d.stage,
                    d.created_at,
                    d.file_path
                FROM documents d
                WHERE d.id = %s
                """,
                (document_id,)
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "filename": row[1],
            "file_size": row[2],
            "page_count": row[3],
            "chunk_count": row[4],
            "status": row[5],
            "stage": row[6],
            "created_at": row[7],
            "file_path": row[8]
        }

    finally:
        connection.close()