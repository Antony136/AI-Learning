from app.retrieval.search import retrieve
from app.retrieval.reranker import rerank


questions = [
    "What is RAG?",
    "What are embeddings?",
    "What is a vector store?",
    "What is fine-tuning?",
    "What is an AI agent?",
    "What is a priority queue?"
]


for question in questions:

    print("\n")
    print("=" * 80)
    print(f"QUESTION: {question}")
    print("=" * 80)

    results = retrieve(
        question,
        top_k=10,
        max_distance=0.50
    )

    if not results:
        print("\nNo vector search results.")
        continue

    print("\nVECTOR SEARCH")
    print("-" * 80)

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"Rank {index} | "
            f"Distance: {result['distance']:.4f} | "
            f"Page: {result['page']} | "
            f"Chunk: {result['chunk_index']}"
        )

    reranked = rerank(
        question,
        results,
        top_n=5
    )

    print("\nRERANKED RESULTS")
    print("-" * 80)

    for index, result in enumerate(
        reranked,
        start=1
    ):

        print(
            f"Rank {index} | "
            f"Score: {result['rerank_score']:.4f} | "
            f"Distance: {result['distance']:.4f} | "
            f"Page: {result['page']} | "
            f"Chunk: {result['chunk_index']}"
        )

        print(
            f"Preview: "
            f"{result['content'][:200]}"
        )