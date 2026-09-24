from app.core.database import get_connection


connection = get_connection()

try:
    with connection.cursor() as cursor:

        # 1. Total number of chunks
        cursor.execute(
            "SELECT COUNT(*) FROM document_chunks"
        )

        total_chunks = cursor.fetchone()[0]

        print("=" * 70)
        print("DATABASE CHECK")
        print("=" * 70)

        print(f"\nTotal chunks: {total_chunks}")

        # 2. Show chunk details
        cursor.execute(
            """
            SELECT
                id,
                source,
                page,
                chunk_index,
                LENGTH(content) AS content_length,
                LEFT(content, 150) AS preview
            FROM document_chunks
            ORDER BY id
            LIMIT 20
            """
        )

        rows = cursor.fetchall()

        print("\nStored chunks:")
        print("=" * 70)

        for row in rows:
            chunk_id = row[0]
            source = row[1]
            page = row[2]
            chunk_index = row[3]
            content_length = row[4]
            preview = row[5]

            print(f"\nID: {chunk_id}")
            print(f"Source: {source}")
            print(f"Page: {page}")
            print(f"Chunk: {chunk_index}")
            print(f"Length: {content_length}")
            print(f"Preview: {preview}")
            print("-" * 70)

        # 3. Check embeddings
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(embedding) AS embeddings
            FROM document_chunks
            """
        )

        total, embeddings = cursor.fetchone()

        print("\nEmbedding check:")
        print("=" * 70)
        print(f"Total chunks: {total}")
        print(f"Chunks with embeddings: {embeddings}")

        if total == embeddings:
            print("✓ Every chunk has an embedding.")
        else:
            print("⚠ Some chunks are missing embeddings.")

finally:
    connection.close()