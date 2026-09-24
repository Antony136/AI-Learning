from app.retrieval.multi_query import multi_query_retrieve


def fake_generate_queries(question, num_queries):
    return [
        "What is RAG?",
        "How does RAG retrieve information?",
        "What is retrieval augmented generation?",
    ]


def fake_generate_embedding(text):
    return [0.1, 0.2, 0.3]


def fake_search_similar_chunks(
    query_embedding,
    top_k,
    max_distance,
    document_ids=None
):
    return [
        {
            "id": 1,
            "document_id": 1,
            "source": "pytest.pdf",
            "page": 1,
            "chunk_index": 1,
            "content": "RAG retrieves relevant information.",
            "distance": 0.20,
        },
        {
            "id": 2,
            "document_id": 1,
            "source": "pytest.pdf",
            "page": 1,
            "chunk_index": 2,
            "content": "RAG uses retrieved context.",
            "distance": 0.30,
        },
    ]


def test_multi_query_retrieve(monkeypatch):
    monkeypatch.setattr(
        "app.retrieval.multi_query.generate_queries",
        fake_generate_queries
    )

    monkeypatch.setattr(
        "app.retrieval.multi_query.generate_embedding",
        fake_generate_embedding
    )

    monkeypatch.setattr(
        "app.retrieval.multi_query.search_similar_chunks",
        fake_search_similar_chunks
    )

    results = multi_query_retrieve(
        question="What is RAG?",
        num_queries=3,
        top_k_per_query=5,
        max_distance=0.50,
    )

    assert isinstance(results, list)
    assert len(results) == 2

    assert results[0]["id"] in [1, 2]
    assert "rrf_score" in results[0]


def test_multi_query_retrieve_passes_document_ids(monkeypatch):
    captured_document_ids = []

    def fake_search(
        query_embedding,
        top_k,
        max_distance,
        document_ids=None
    ):
        captured_document_ids.append(document_ids)

        return [
            {
                "id": 1,
                "document_id": 5,
                "source": "pytest.pdf",
                "page": 1,
                "chunk_index": 1,
                "content": "RAG retrieves information.",
                "distance": 0.20,
            }
        ]

    monkeypatch.setattr(
        "app.retrieval.multi_query.generate_queries",
        fake_generate_queries
    )

    monkeypatch.setattr(
        "app.retrieval.multi_query.generate_embedding",
        fake_generate_embedding
    )

    monkeypatch.setattr(
        "app.retrieval.multi_query.search_similar_chunks",
        fake_search
    )

    multi_query_retrieve(
        question="What is RAG?",
        num_queries=3,
        top_k_per_query=5,
        max_distance=0.50,
        document_ids=[5, 7],
    )

    assert len(captured_document_ids) == 3

    assert all(
        document_ids == [5, 7]
        for document_ids in captured_document_ids
    )