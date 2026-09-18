from ollama import embed


text = "RAG retrieves relevant information before generating an answer."


response = embed(
    model="nomic-embed-text",
    input=text
)

vector = response.embeddings[0]

print("Text:")
print(text)

print("\nVector dimension:")
print(len(vector))

print("\nFirst 10 values:")
print(vector[:10])