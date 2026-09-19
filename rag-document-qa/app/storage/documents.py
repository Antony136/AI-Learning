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
                    d.created_at,
                    COUNT(c.id) AS chunk_count
                FROM documents d
                LEFT JOIN document_chunks c
                    ON c.document_id = d.id
                GROUP BY
                    d.id,
                    d.filename,
                    d.created_at
                ORDER BY d.created_at DESC
                """
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "filename": row[1],
                "created_at": row[2],
                "chunk_count": row[3]
            }
            for row in rows
        ]

    finally:
        connection.close()