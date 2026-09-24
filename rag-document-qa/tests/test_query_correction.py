from app.retrieval.query_correction import (
    similarity,
    edit_distance,
    is_suspicious_word,
    find_best_candidate,
    correct_query,
)


def test_similarity_identical_words():
    assert similarity("RAG", "RAG") == 1.0


def test_edit_distance():
    assert edit_distance("cat", "cat") == 0
    assert edit_distance("cat", "cut") == 1
    assert edit_distance("cat", "cats") == 1


def test_short_word_is_not_suspicious():
    assert is_suspicious_word("is") is False
    assert is_suspicious_word("RAG") is False


def test_common_word_is_not_suspicious():
    assert is_suspicious_word("what") is False
    assert is_suspicious_word("explain") is False


def test_word_with_digits_is_not_suspicious():
    assert is_suspicious_word("python3") is False


def test_existing_vocabulary_word_is_not_corrected():
    vocabulary = {"rag", "embeddings", "differential"}

    result = find_best_candidate(
        "rag",
        vocabulary,
    )

    assert result is None


def test_find_best_candidate():
    vocabulary = {
        "rag",
        "embeddings",
        "differential",
        "calculus",
    }

    result = find_best_candidate(
        "Differtial",
        vocabulary,
        similarity_threshold=0.90,
        max_edit_distance=2,
    )

    assert result is not None
    assert result["original"] == "Differtial"
    assert result["corrected"] == "differential"
    assert result["edit_distance"] <= 2
    assert result["score"] >= 0.90


def test_find_best_candidate_rejects_dissimilar_word():
    vocabulary = {
        "rag",
        "embeddings",
        "differential",
    }

    result = find_best_candidate(
        "quantum",
        vocabulary,
        similarity_threshold=0.90,
        max_edit_distance=2,
    )

    assert result is None


def test_correct_query():
    vocabulary = {
        "rag",
        "embeddings",
        "differential",
        "calculus",
    }

    corrected_query, corrections = correct_query(
        "What are the applications of Differtial Calculus?",
        vocabulary,
        similarity_threshold=0.90,
        max_edit_distance=2,
    )

    assert corrected_query == (
        "What are the applications of differential Calculus?"
    )

    assert len(corrections) == 1
    assert corrections[0]["original"] == "Differtial"
    assert corrections[0]["corrected"] == "differential"


def test_correct_query_preserves_unknown_words():
    vocabulary = {
        "rag",
        "embeddings",
        "differential",
    }

    corrected_query, corrections = correct_query(
        "What is Kubernetes?",
        vocabulary,
        similarity_threshold=0.90,
        max_edit_distance=2,
    )

    assert corrected_query == "What is Kubernetes?"
    assert corrections == []