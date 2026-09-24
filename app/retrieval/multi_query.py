from app.retrieval.query_transform import generate_queries
from app.ingestion.embeddings import generate_embedding
from app.retrieval.vector_store import search_similar_chunks
from app.retrieval.fusion import reciprocal_rank_fusion


def multi_query_retrieve(
    question: str,
    num_queries: int = 3,
    top_k_per_query: int = 5,
    max_distance: float = 0.50,
    document_ids: list[int] | None = None
):
    queries = generate_queries(
        question,
        num_queries=num_queries
    )

    print("\n" + "=" * 70)
    print("GENERATED QUERIES")
    print("=" * 70)

    for index, query in enumerate(queries, start=1):
        print(f"Query {index}: {query}")

    result_lists = []

    for query in queries:
        query_embedding = generate_embedding(query)

        results = search_similar_chunks(
            query_embedding,
            top_k=top_k_per_query,
            max_distance=max_distance,
            document_ids=document_ids
        )

        result_lists.append(results)

    fused_results = reciprocal_rank_fusion(
        result_lists
    )

    return fused_results