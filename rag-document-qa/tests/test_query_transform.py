from app.retrieval.query_transform import generate_queries


class FakeMessage:
    content = (
        "What is retrieval augmented generation?\n"
        "How does RAG retrieve relevant information?\n"
        "What is the purpose of RAG?"
    )


class FakeResponse:
    message = FakeMessage()


def fake_chat(*args, **kwargs):
    return FakeResponse()


def test_generate_queries(monkeypatch):
    monkeypatch.setattr(
        "app.retrieval.query_transform.chat",
        fake_chat
    )

    queries = generate_queries(
        "What is RAG?",
        num_queries=3
    )

    assert isinstance(queries, list)
    assert len(queries) == 3

    assert queries[0] == (
        "What is retrieval augmented generation?"
    )

    assert queries[1] == (
        "How does RAG retrieve relevant information?"
    )

    assert queries[2] == (
        "What is the purpose of RAG?"
    )


def test_generate_queries_respects_num_queries(monkeypatch):
    monkeypatch.setattr(
        "app.retrieval.query_transform.chat",
        fake_chat
    )

    queries = generate_queries(
        "What is RAG?",
        num_queries=2
    )

    assert len(queries) == 2

    assert queries == [
        "What is retrieval augmented generation?",
        "How does RAG retrieve relevant information?",
    ]