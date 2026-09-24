from ollama import embed
import math


def get_embedding(text: str):
    response = embed(
        model="nomic-embed-text",
        input=text
    )

    return response.embeddings[0]


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


text_a = "RAG retrieves relevant documents before generating an answer."

text_b = "Retrieval augmented generation finds useful information before answering."

text_c = "The weather is very hot today."


embedding_a = get_embedding(text_a)
embedding_b = get_embedding(text_b)
embedding_c = get_embedding(text_c)


print("A vs B:")
print(cosine_similarity(embedding_a, embedding_b))


print("\nA vs C:")
print(cosine_similarity(embedding_a, embedding_c))