from app.retrieval.reranker import rerank


def test_reranker_prioritizes_relevant_result():
    question = "What is RAG?"

    results = [
        {
            "id": 1,
            "document_id": 1,
            "source": "pytest_reranking.pdf",
            "page": 1,
            "chunk_index": 1,
            "content": (
                "RAG retrieves relevant information from documents "
                "and provides that information to a language model."
            ),
            "distance": 0.30,
        },
        {
            "id": 2,
            "document_id": 1,
            "source": "pytest_reranking.pdf",
            "page": 1,
            "chunk_index": 2,
            "content": (
                "Priority queues store elements according to their "
                "priority and are commonly implemented using heaps."
            ),
            "distance": 0.20,
        },
        {
            "id": 3,
            "document_id": 1,
            "source": "pytest_reranking.pdf",
            "page": 1,
            "chunk_index": 3,
            "content": (
                "Fine-tuning adapts a pretrained language model "
                "using additional training data."
            ),
            "distance": 0.25,
        },
    ]

    reranked = rerank(
        question=question,
        results=results,
        top_n=3,
    )

    assert isinstance(reranked, list)
    assert len(reranked) == 3

    assert "rerank_score" in reranked[0]

    assert reranked[0]["content"] == (
        "RAG retrieves relevant information from documents "
        "and provides that information to a language model."
    )