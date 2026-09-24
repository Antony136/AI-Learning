from app.retrieval.multi_query import multi_query_retrieve


question = "What is RAG?"

results = multi_query_retrieve(
    question,
    num_queries=3,
    top_k_per_query=5,
    document_ids=[2]
)


print("\n" + "=" * 70)
print("MULTI-QUERY RETRIEVAL TEST")
print("=" * 70)

print("\nQuestion:")
print(question)

print("\nFused Results:")

for index, result in enumerate(results, start=1):
    print("\n" + "-" * 70)

    print("Rank:", index)
    print("Document ID:", result["document_id"])
    print("Page:", result["page"])
    print("Chunk:", result["chunk_index"])
    print("Distance:", result["distance"])
    print("RRF Score:", result["rrf_score"])

    print("\nContent:")
    print(result["content"][:500])