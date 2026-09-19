from ollama import embed


EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text: str):
    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.embeddings[0]