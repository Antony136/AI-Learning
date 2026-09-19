from app.retrieval.query_transform import generate_queries


questions = [
    "What is RAG?",
    "What are embeddings?",
    "What is a vector store?"
]


for question in questions:
    print("\n" + "=" * 70)
    print(f"Original question: {question}")
    print("=" * 70)

    queries = generate_queries(question)

    for index, query in enumerate(queries, start=1):
        print(f"{index}. {query}")