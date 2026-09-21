from app.ingestion.embeddings import generate_embedding
from app.retrieval.vector_store import search_similar_chunks
from app.retrieval.reranker import rerank


QUESTIONS = [
    "Differential",
    "Differtial",
    "differential calculus",
    "applications of differential calculus"
]

DOCUMENT_ID = 3


def test_query(question: str):
    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    # Step 1: Convert question into embedding
    query_embedding = generate_embedding(question)

    # Step 2: Retrieve candidates
    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=10,
        max_distance=0.50,
        document_id=DOCUMENT_ID
    )

    print(f"\nVector results: {len(results)}")

    if not results:
        print("No vector results found.")
        return

    # Show vector retrieval
    print("\n--- Vector Retrieval ---")

    for i, result in enumerate(results, start=1):
        print(
            f"{i}. "
            f"Page {result['page']} | "
            f"Chunk {result['chunk_index']} | "
            f"Distance: {result['distance']:.4f}"
        )

    # Step 3: Rerank
    reranked = rerank(
        question=question,
        results=results,
        top_n=5
    )

    print("\n--- Reranked Results ---")

    for i, result in enumerate(reranked, start=1):
        print(
            f"{i}. "
            f"Page {result['page']} | "
            f"Chunk {result['chunk_index']} | "
            f"Rerank Score: {result['rerank_score']:.4f}"
        )

        print(
            f"   {result['content'][:200].replace(chr(10), ' ')}..."
        )


if __name__ == "__main__":

    for question in QUESTIONS:
        test_query(question)