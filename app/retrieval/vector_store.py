from app.core.database import get_connection


def search_similar_chunks(
    query_embedding,
    top_k=5,
    max_distance=0.50,
    document_ids=None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if document_ids is not None:

                if not document_ids:
                    return []

                placeholders = ", ".join(
                    ["%s"] * len(document_ids)
                )

                query = f"""
                    SELECT
                        id,
                        document_id,
                        source,
                        page,
                        chunk_index,
                        content,
                        embedding <=> %s::vector AS distance
                    FROM document_chunks
                    WHERE document_id IN ({placeholders})
                      AND embedding <=> %s::vector <= %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """

                parameters = (
                    [query_embedding]
                    + document_ids
                    + [
                        query_embedding,
                        max_distance,
                        query_embedding,
                        top_k
                    ]
                )

                cursor.execute(
                    query,
                    parameters
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

        return [
            {
                "id": row[0],
                "document_id": row[1],
                "source": row[2],
                "page": row[3],
                "chunk_index": row[4],
                "content": row[5],
                "distance": row[6]
            }
            for row in rows
        ]

    finally:
        connection.close()