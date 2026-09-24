from app.core.database import get_connection


def search_experiment_chunks(
    query_embedding: list[float],
    chunk_size: int,
    overlap_sentences: int = 1,
    top_k: int = 5
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
                    chunk_size,
                    overlap_sentences,
                    content,
                    embedding <=> %s::vector AS distance
                FROM document_chunks_experiment
                WHERE chunk_size = %s
                  AND overlap_sentences = %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    query_embedding,
                    chunk_size,
                    overlap_sentences,
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
                    "source": row[1],
                    "page": row[2],
                    "chunk_index": row[3],
                    "chunk_size": row[4],
                    "overlap_sentences": row[5],
                    "content": row[6],
                    "distance": row[7]
                }
            )

        return results

    finally:
        connection.close()