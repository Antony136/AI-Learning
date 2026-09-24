from app.retrieval.search import retrieve


questions = [
    "What is RAG?",
    "What are embeddings?",
    "What is fine-tuning?",
    "What is a vector store?",
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
        top_k=5,
        max_distance=0.50
    )

    if not results:
        print("No relevant chunks found.")
        continue

    for index, result in enumerate(results, start=1):

        print(
            f"\nRank {index}"
        )

        print(
            f"Distance: {result['distance']:.4f}"
        )

        print(
            f"Page: {result['page']} | "
            f"Chunk: {result['chunk_index']}"
        )

        print(
            f"Preview: "
            f"{result['content'][:250].replace(chr(10), ' ')}"
        )