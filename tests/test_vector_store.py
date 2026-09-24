from ollama import embed

from app.retrieval.vector_store import search_similar_chunks
from app.storage.chunks import create_document, insert_chunk


EMBEDDING_MODEL = "nomic-embed-text"


def get_embedding(text: str):
    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.embeddings[0]


def test_vector_search_returns_results():

    document_id = create_document(
        "pytest_vector_search.pdf"
    )

    content = (
        "RAG retrieves relevant information "
        "from documents before generating an answer."
    )

    embedding = get_embedding(content)

    insert_chunk(
        document_id=document_id,
        source="pytest_vector_search.pdf",
        page=1,
        chunk_index=1,
        content=content,
        embedding=embedding
    )

    query = "How does RAG retrieve information?"

    query_embedding = get_embedding(query)

    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=3,
        max_distance=0.50
    )

    assert isinstance(results, list)
    assert len(results) > 0

    assert results[0]["document_id"] == document_id
    assert results[0]["content"] == content


def test_vector_search_result_structure():

    document_id = create_document(
        "pytest_vector_structure.pdf"
    )

    content = (
        "RAG combines retrieval with language model generation."
    )

    embedding = get_embedding(content)

    insert_chunk(
        document_id=document_id,
        source="pytest_vector_structure.pdf",
        page=1,
        chunk_index=1,
        content=content,
        embedding=embedding
    )

    query_embedding = get_embedding(
        "What does RAG combine?"
    )

    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=3,
        max_distance=0.50
    )

    assert isinstance(results, list)

    for result in results:
        assert "id" in result
        assert "document_id" in result
        assert "source" in result
        assert "page" in result
        assert "chunk_index" in result
        assert "content" in result
        assert "distance" in result