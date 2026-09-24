from app.rag import RERANK_THRESHOLD


def test_reranker_threshold_value():
    assert RERANK_THRESHOLD == 1.0


def test_score_above_threshold_is_accepted():
    score = 1.5

    assert score >= RERANK_THRESHOLD


def test_score_below_threshold_is_rejected():
    score = 0.5

    assert score < RERANK_THRESHOLD