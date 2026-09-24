from app.retrieval.search import retrieve
from app.retrieval.reranker import rerank


DOCUMENT_ID = 3

QUERIES = [
    "What are the applications of Differtial Calculus?",
    "What are the applications of Differential Calculus?"
]


for query in QUERIES:

    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retrieve(
        question=query,
        top_k=10,
        max_distance=0.50,
        document_id=DOCUMENT_ID
    )

    print("\nVECTOR RETRIEVAL")
    print("-" * 80)

    for result in results:
        print(
            f"Page {result['page']:<4} "
            f"Chunk {result['chunk_index']:<3} "
            f"Distance: {result['distance']:.4f}"
        )

    reranked = rerank(
        question=query,
        results=results,
        top_n=5
    )

    print("\nRERANKING")
    print("-" * 80)

    for result in reranked:
        print(
            f"Page {result['page']:<4} "
            f"Chunk {result['chunk_index']:<3} "
            f"Rerank score: {result['rerank_score']:.4f}"
        )