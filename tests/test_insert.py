from ollama import embed

from app.storage.chunks import create_document, insert_chunk


def test_insert_chunk():

    text = "RAG retrieves relevant information before generating an answer."

    response = embed(
        model="nomic-embed-text",
        input=text
    )

    embedding = response.embeddings[0]

    document_id = create_document("test.txt")

    insert_chunk(
        document_id=document_id,
        source="test.txt",
        page=1,
        chunk_index=1,
        content=text,
        embedding=embedding
    )

    assert document_id is not None