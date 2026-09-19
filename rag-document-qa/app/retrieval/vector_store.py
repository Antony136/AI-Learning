from app.core.database import get_connection


def search_similar_chunks(
    query_embedding: list[float],
    top_k: int = 5,
    max_distance: float = 0.50
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    source,
                    page,
                    chunk_index,
                    content,
                    embedding <=> %s::vector AS distance
                FROM document_chunks
                WHERE embedding <=> %s::vector <= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    query_embedding,
                    query_embedding,
                    max_distance,
                    query_embedding,
                    top_k
                )
            )

            rows = cursor.fetchall()

        results = []

        for row in rows:
            results.append({
                "id": row[0],
                "source": row[1],
                "page": row[2],
                "chunk_index": row[3],
                "content": row[4],
                "distance": row[5]
            })

        return results

    finally:
        connection.close()