def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int = 60
):
    scores = {}
    results_by_id = {}

    for results in result_lists:
        for rank, result in enumerate(
            results,
            start=1
        ):
            result_id = result["id"]

            score = 1 / (k + rank)

            scores[result_id] = (
                scores.get(result_id, 0)
                + score
            )

            results_by_id[result_id] = result

    fused_results = []

    for result_id, score in scores.items():
        fused_results.append(
            {
                **results_by_id[result_id],
                "rrf_score": score
            }
        )

    fused_results.sort(
        key=lambda x: x["rrf_score"],
        reverse=True
    )

    return fused_results