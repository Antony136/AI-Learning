from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_reranker = None


def get_reranker():
    global _reranker

    if _reranker is None:
        _reranker = CrossEncoder(MODEL_NAME)

    return _reranker


def rerank(
    question: str,
    results: list[dict],
    top_n: int = 5
):
    if not results:
        return []

    pairs = [
        (
            question,
            result["content"]
        )
        for result in results
    ]

    reranker = get_reranker()

    scores = reranker.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):
        reranked.append(
            {
                **result,
                "rerank_score": float(score)
            }
        )

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked[:top_n]