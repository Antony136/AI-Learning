from app.rag import answer_question


def test_answer_question_returns_answer(monkeypatch):
    monkeypatch.setattr(
        "app.rag.normalize_query",
        lambda question: question
    )

    monkeypatch.setattr(
        "app.rag.rewrite_question",
        lambda question, conversation: question
    )

    monkeypatch.setattr(
        "app.rag.improve_query",
        lambda question, document_ids, retrieval_top_k, final_top_n: question
    )

    monkeypatch.setattr(
        "app.rag.multi_query_retrieve",
        lambda **kwargs: [
            {
                "id": 1,
                "document_id": 1,
                "source": "pytest.pdf",
                "page": 1,
                "chunk_index": 1,
                "content": "RAG retrieves relevant information from documents.",
                "distance": 0.20,
                "rrf_score": 0.03,
            }
        ]
    )

    monkeypatch.setattr(
        "app.rag.rerank",
        lambda question, results, top_n: [
            {
                **results[0],
                "rerank_score": 2.0,
            }
        ]
    )

    monkeypatch.setattr(
        "app.rag.build_context",
        lambda results: "RAG retrieves relevant information from documents."
    )

    monkeypatch.setattr(
        "app.rag.generate_answer",
        lambda question, context: "RAG retrieves relevant information before generating an answer."
    )

    answer, sources = answer_question("What is RAG?")

    assert answer == (
        "RAG retrieves relevant information before generating an answer."
    )

    assert len(sources) == 1
    assert sources[0]["id"] == 1
    assert sources[0]["rerank_score"] == 2.0


def test_answer_question_returns_fallback_when_no_results(monkeypatch):
    monkeypatch.setattr(
        "app.rag.normalize_query",
        lambda question: question
    )

    monkeypatch.setattr(
        "app.rag.rewrite_question",
        lambda question, conversation: question
    )

    monkeypatch.setattr(
        "app.rag.improve_query",
        lambda question, document_ids, retrieval_top_k, final_top_n: question
    )

    monkeypatch.setattr(
        "app.rag.multi_query_retrieve",
        lambda **kwargs: []
    )

    answer, sources = answer_question("What is RAG?")

    assert answer == (
        "I could not find relevant information in the selected documents."
    )

    assert sources == []


def test_answer_question_rejects_low_rerank_score(monkeypatch):
    monkeypatch.setattr(
        "app.rag.normalize_query",
        lambda question: question
    )

    monkeypatch.setattr(
        "app.rag.rewrite_question",
        lambda question, conversation: question
    )

    monkeypatch.setattr(
        "app.rag.improve_query",
        lambda question, document_ids, retrieval_top_k, final_top_n: question
    )

    monkeypatch.setattr(
        "app.rag.multi_query_retrieve",
        lambda **kwargs: [
            {
                "id": 1,
                "document_id": 1,
                "source": "pytest.pdf",
                "page": 1,
                "chunk_index": 1,
                "content": "Unrelated information.",
                "distance": 0.40,
                "rrf_score": 0.02,
            }
        ]
    )

    monkeypatch.setattr(
        "app.rag.rerank",
        lambda question, results, top_n: [
            {
                **results[0],
                "rerank_score": 0.5,
            }
        ]
    )

    answer, sources = answer_question("What is RAG?")

    assert answer == (
        "I could not find relevant information in the selected documents."
    )

    assert sources == []


def test_answer_question_passes_conversation_to_rewriter(monkeypatch):
    captured = {}

    monkeypatch.setattr(
        "app.rag.normalize_query",
        lambda question: question
    )

    def fake_rewrite(question, conversation):
        captured["question"] = question
        captured["conversation"] = conversation
        return question

    monkeypatch.setattr(
        "app.rag.rewrite_question",
        fake_rewrite
    )

    monkeypatch.setattr(
        "app.rag.improve_query",
        lambda question, document_ids, retrieval_top_k, final_top_n: question
    )

    monkeypatch.setattr(
        "app.rag.multi_query_retrieve",
        lambda **kwargs: []
    )

    conversation = [
        {
            "role": "user",
            "content": "What is RAG?"
        },
        {
            "role": "assistant",
            "content": "RAG retrieves information."
        }
    ]

    answer_question(
        "How does it work?",
        conversation=conversation
    )

    assert captured["question"] == "How does it work?"
    assert captured["conversation"] == conversation


def test_improve_query_returns_original_when_no_correction(monkeypatch):
    from app.rag import improve_query

    monkeypatch.setattr(
        "app.rag.get_document_vocabulary",
        lambda document_ids: {"rag", "retrieval", "generation"}
    )

    monkeypatch.setattr(
        "app.rag.correct_query",
        lambda question, vocabulary, similarity_threshold, max_edit_distance:
            (question, [])
    )

    question = "What is RAG?"

    result = improve_query(question)

    assert result == question


def test_improve_query_accepts_better_correction(monkeypatch):
    from app.rag import improve_query

    monkeypatch.setattr(
        "app.rag.get_document_vocabulary",
        lambda document_ids: {
            "differential",
            "equation",
            "calculus"
        }
    )

    monkeypatch.setattr(
        "app.rag.correct_query",
        lambda question, vocabulary, similarity_threshold, max_edit_distance:
            (
                "What is differential equation?",
                [
                    {
                        "original": "differntial",
                        "corrected": "differential",
                        "score": 0.95,
                        "edit_distance": 1,
                    }
                ],
            )
    )

    def fake_retrieve(question, top_k, max_distance, document_ids):
        return [
            {
                "id": 1,
                "document_id": 1,
                "source": "pytest.pdf",
                "page": 1,
                "chunk_index": 1,
                "content": "Differential equations describe relationships between variables.",
                "distance": 0.20,
            }
        ]

    monkeypatch.setattr(
        "app.rag.retrieve",
        fake_retrieve
    )

    def fake_rerank(question, results, top_n):
        score = 1.0 if "differntial" in question else 4.0

        return [
            {
                **results[0],
                "rerank_score": score,
            }
        ]

    monkeypatch.setattr(
        "app.rag.rerank",
        fake_rerank
    )

    result = improve_query(
        "What is differntial equation?"
    )

    assert result == "What is differential equation?"


def test_improve_query_rejects_insufficient_improvement(monkeypatch):
    from app.rag import improve_query

    monkeypatch.setattr(
        "app.rag.get_document_vocabulary",
        lambda document_ids: {
            "differential",
            "equation",
            "calculus"
        }
    )

    monkeypatch.setattr(
        "app.rag.correct_query",
        lambda question, vocabulary, similarity_threshold, max_edit_distance:
            (
                "What is differential equation?",
                [
                    {
                        "original": "differntial",
                        "corrected": "differential",
                        "score": 0.95,
                        "edit_distance": 1,
                    }
                ],
            )
    )

    def fake_retrieve(question, top_k, max_distance, document_ids):
        return [
            {
                "id": 1,
                "document_id": 1,
                "source": "pytest.pdf",
                "page": 1,
                "chunk_index": 1,
                "content": "Differential equations describe relationships between variables.",
                "distance": 0.20,
            }
        ]

    monkeypatch.setattr(
        "app.rag.retrieve",
        fake_retrieve
    )

    def fake_rerank(question, results, top_n):
        score = 2.0 if "differntial" in question else 3.0

        return [
            {
                **results[0],
                "rerank_score": score,
            }
        ]

    monkeypatch.setattr(
        "app.rag.rerank",
        fake_rerank
    )

    result = improve_query(
        "What is differntial equation?"
    )

    assert result == "What is differntial equation?"