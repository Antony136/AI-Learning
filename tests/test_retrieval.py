from ollama import embed

from app.retrieval.search import retrieve
from app.storage.chunks import create_document, insert_chunk


EMBEDDING_MODEL = "nomic-embed-text"


def get_embedding(text: str):
    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.embeddings[0]


def test_retrieve_returns_relevant_chunk():

    document_id = create_document(
        "pytest_retrieval.pdf"
    )

    content = (
        "RAG retrieves relevant information from documents "
        "before generating an answer."
    )

    embedding = get_embedding(content)

    insert_chunk(
        document_id=document_id,
        source="pytest_retrieval.pdf",
        page=1,
        chunk_index=1,
        content=content,
        embedding=embedding
    )

    results = retrieve(
        question="How does RAG retrieve information?",
        top_k=3,
        max_distance=0.50
    )

    assert isinstance(results, list)
    assert len(results) > 0

    assert results[0]["document_id"] == document_id
    assert results[0]["content"] == content