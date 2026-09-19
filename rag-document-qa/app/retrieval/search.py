from app.ingestion.embeddings import generate_embedding
from app.retrieval.vector_store import search_similar_chunks


def retrieve(
    question: str,
    top_k: int = 5,
    max_distance: float = 0.50
):
    query_embedding = generate_embedding(question)

    return search_similar_chunks(
        query_embedding,
        top_k=top_k,
        max_distance=max_distance
    )


if __name__ == "__main__":
    question = input("Question: ")

    results = retrieve(
        question,
        top_k=5,
        max_distance=0.50
    )

    print("\nRelevant chunks:")
    print("=" * 70)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Page: {result['page']}")
        print(f"Chunk: {result['chunk_index']}")

        print("\n" + result["content"])
        print("=" * 70)