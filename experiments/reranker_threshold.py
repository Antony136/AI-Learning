from app.retrieval.search import retrieve
from app.retrieval.reranker import rerank


test_questions = [
    # Questions that should be answerable from the document
    {
        "question": "What is GenAI?",
        "expected": "ANSWERABLE"
    },
    {
        "question": "What is RAG?",
        "expected": "ANSWERABLE"
    },
    {
        "question": "What are embeddings?",
        "expected": "ANSWERABLE"
    },
    {
        "question": "What is a vector store?",
        "expected": "ANSWERABLE"
    },
    {
        "question": "What is fine-tuning?",
        "expected": "ANSWERABLE"
    },

    # Questions that should NOT be answerable
    {
        "question": "What is an AI agent?",
        "expected": "NOT ANSWERABLE"
    },
    {
        "question": "What is a priority queue?",
        "expected": "NOT ANSWERABLE"
    },
    {
        "question": "What is Kubernetes?",
        "expected": "NOT ANSWERABLE"
    },
    {
        "question": "What is quantum computing?",
        "expected": "NOT ANSWERABLE"
    },
    {
        "question": "What is Docker Compose?",
        "expected": "NOT ANSWERABLE"
    }
]


for item in test_questions:

    question = item["question"]
    expected = item["expected"]

    print("\n")
    print("=" * 80)
    print(f"QUESTION: {question}")
    print(f"EXPECTED: {expected}")
    print("=" * 80)

    results = retrieve(
        question,
        top_k=10,
        max_distance=0.50
    )

    if not results:
        print("\nNo vector search results.")
        continue

    reranked = rerank(
        question,
        results,
        top_n=5
    )

    if not reranked:
        print("\nNo reranked results.")
        continue

    best_score = reranked[0]["rerank_score"]

    print("\nRERANKER SCORES")
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

    print("\nBEST SCORE")
    print("-" * 80)
    print(f"{best_score:.4f}")