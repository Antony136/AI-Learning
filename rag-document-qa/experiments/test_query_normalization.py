from app.retrieval.query_normalization import normalize_query


test_queries = [
    "   WHAT IS RAG???   ",
    "What   is    retrieval   augmented   generation?",
    "WHY IS RAG USEFUL????",
    "   explain embeddings   ",
]


for query in test_queries:
    normalized = normalize_query(query)

    print("Original:  ", query)
    print("Normalized:", normalized)
    print("-" * 60)