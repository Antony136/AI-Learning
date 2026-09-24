from app.retrieval.multi_query import multi_query_retrieve


questions = [
    "What is RAG?",
    "What are embeddings?",
    "What is a vector store?"
]


for question in questions:
    print("\n" + "=" * 70)
    print(f"Question: {question}")
    print("=" * 70)

    results = multi_query_retrieve(
        question,
        num_queries=3,
        top_k_per_query=5,
        max_distance=0.50
    )

    print(f"\nUnique retrieved chunks: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(
            f"\nResult {index}"
        )

        print(
            f"Page: {result['page']} | "
            f"Chunk: {result['chunk_index']} | "
            f"RRF score: {result['rrf_score']:.6f}"
        )

        print(
            result["content"][:300]
        )