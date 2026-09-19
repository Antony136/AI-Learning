from app.ingestion.embeddings import generate_embedding
from app.retrieval.vector_store import search_similar_chunks


question = "What is RAG?"


query_embedding = generate_embedding(question)


results = search_similar_chunks(
    query_embedding,
    top_k=5
)


print("\nQuestion:")
print(question)

print("\nRetrieved chunks:")
print("=" * 70)


for index, result in enumerate(results, start=1):

    print(f"\nResult {index}")
    print(f"Distance: {result['distance']:.4f}")
    print(f"Source: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Chunk: {result['chunk_index']}")

    print("\nContent:")
    print(result["content"])

    print("=" * 70)