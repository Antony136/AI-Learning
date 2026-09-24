import pytest
from app.retrieval.fusion import reciprocal_rank_fusion


def test_rrf_combines_results():
    result_lists = [
        [
            {"id": 1, "content": "Chunk A"},
            {"id": 2, "content": "Chunk B"},
            {"id": 3, "content": "Chunk C"},
        ],
        [
            {"id": 2, "content": "Chunk B"},
            {"id": 4, "content": "Chunk D"},
            {"id": 1, "content": "Chunk A"},
        ],
    ]

    results = reciprocal_rank_fusion(
        result_lists,
        k=60
    )

    assert isinstance(results, list)
    assert len(results) == 4


def test_rrf_duplicate_results_are_merged():
    result_lists = [
        [
            {"id": 1, "content": "Chunk A"},
        ],
        [
            {"id": 1, "content": "Chunk A"},
        ],
    ]

    results = reciprocal_rank_fusion(
        result_lists,
        k=60
    )

    assert len(results) == 1
    assert results[0]["id"] == 1


def test_rrf_duplicate_results_accumulate_score():
    result_lists = [
        [
            {"id": 1, "content": "Chunk A"},
        ],
        [
            {"id": 1, "content": "Chunk A"},
        ],
    ]

    results = reciprocal_rank_fusion(
        result_lists,
        k=60
    )

    expected_score = (1 / 61) + (1 / 61)

    assert results[0]["rrf_score"] == pytest.approx(expected_score)


def test_rrf_results_are_sorted_by_score():
    result_lists = [
        [
            {"id": 1, "content": "Chunk A"},
            {"id": 2, "content": "Chunk B"},
        ],
        [
            {"id": 2, "content": "Chunk B"},
        ],
    ]

    results = reciprocal_rank_fusion(
        result_lists,
        k=60
    )

    assert results[0]["id"] == 2
    assert results[1]["id"] == 1


def test_rrf_empty_results():
    results = reciprocal_rank_fusion(
        [],
        k=60
    )

    assert results == []