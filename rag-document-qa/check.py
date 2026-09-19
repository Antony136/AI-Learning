from app.retrieval.search import retrieve

results = retrieve(
    "What is RAG?",
    document_id=2
)

for result in results:
    print(
        result["document_id"],
        result["page"],
        result["chunk_index"]
    )