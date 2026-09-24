from app.retrieval.query_rewriter import rewrite_query


class FakeMessage:
    content = "What are the applications of Differential Calculus?"


class FakeResponse:
    message = FakeMessage()


def fake_chat(*args, **kwargs):
    return FakeResponse()


def test_rewrite_query(monkeypatch):
    monkeypatch.setattr(
        "app.retrieval.query_rewriter.chat",
        fake_chat
    )

    rewritten = rewrite_query(
        "What are the applications of Differtial Calculus?"
    )

    assert rewritten == (
        "What are the applications of Differential Calculus?"
    )


def test_rewrite_query_returns_clean_text(monkeypatch):
    monkeypatch.setattr(
        "app.retrieval.query_rewriter.chat",
        fake_chat
    )

    rewritten = rewrite_query("Differtial")

    assert isinstance(rewritten, str)
    assert rewritten.strip() == rewritten
    assert rewritten != ""