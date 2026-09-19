from app.core.database import get_connection


def search_similar_chunks(
    query_embedding: list[float],
    top_k: int = 5,
    max_distance: float = 0.50,
    document_id: int | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if document_id is not None:

                cursor.execute(
                    """
                    SELECT
                        id,
                        document_id,
                        source,
                        page,
                        chunk_index,
                        content,
                        embedding <=> %s::vector AS distance
                    FROM document_chunks
                    WHERE document_id = %s
                      AND embedding <=> %s::vector <= %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        query_embedding,
                        document_id,
                        query_embedding,
                        max_distance,
                        query_embedding,
                        top_k
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        id,
                        document_id,
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
            results.append(
                {
                    "id": row[0],
                    "document_id": row[1],
                    "source": row[2],
                    "page": row[3],
                    "chunk_index": row[4],
                    "content": row[5],
                    "distance": row[6]
                }
            )

        return results

    finally:
        connection.close()