from ollama import embed

from app.storage.chunks import insert_chunk


text = "RAG retrieves relevant information before generating an answer."


response = embed(
    model="nomic-embed-text",
    input=text
)

embedding = response.embeddings[0]


insert_chunk(
    source="test.txt",
    page=1,
    chunk_index=1,
    content=text,
    embedding=embedding
)

print("Chunk inserted successfully!")