from types import SimpleNamespace

from app.retrieval.query_rewrite import rewrite_question


class FakeMessage:
    content = "Why is RAG useful?"


class FakeResponse:
    message = FakeMessage()


def fake_chat(*args, **kwargs):
    return FakeResponse()


def test_rewrite_question_with_conversation(monkeypatch):
    monkeypatch.setattr(
        "app.retrieval.query_rewrite.chat",
        fake_chat
    )

    conversation = [
        SimpleNamespace(
            role="user",
            content="What is RAG?"
        ),
        SimpleNamespace(
            role="assistant",
            content="RAG retrieves relevant information from documents."
        ),
    ]

    rewritten = rewrite_question(
        "Why is it useful?",
        conversation
    )

    assert rewritten == "Why is RAG useful?"


def test_rewrite_question_without_conversation():
    conversation = []

    question = "Why is it useful?"

    rewritten = rewrite_question(
        question,
        conversation
    )

    assert rewritten == question