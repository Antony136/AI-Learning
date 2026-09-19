from ollama import embed

from app.retrieval.vector_store import VectorStore


EMBEDDING_MODEL = "nomic-embed-text"


def get_embedding(text: str):
    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.embeddings[0]


store = VectorStore()


documents = [
    "RAG retrieves relevant information before generating an answer.",
    "Embeddings represent the semantic meaning of text as vectors.",
    "Python is a popular programming language.",
    "PostgreSQL is a relational database system.",
    "Large language models generate text based on learned patterns."
]


for document in documents:

    embedding = get_embedding(document)

    store.add(
        text=document,
        embedding=embedding
    )


query = "How does RAG find information?"


query_embedding = get_embedding(query)


results = store.search(
    query_embedding,
    top_k=3
)


print("Query:")
print(query)

print("\nMost relevant documents:\n")


for index, result in enumerate(results, start=1):

    print(f"{index}. Score: {result['score']:.4f}")
    print(f"   {result['text']}")
    print()