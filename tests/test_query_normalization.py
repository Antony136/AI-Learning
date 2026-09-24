from app.retrieval.query_normalization import normalize_query


def test_normalize_whitespace():
    query = "   What   is   RAG?   "

    result = normalize_query(query)

    assert result == "what is rag?"


def test_normalize_case():
    query = "What Is RAG?"

    result = normalize_query(query)

    assert result == "what is rag?"


def test_normalize_repeated_question_marks():
    query = "What is RAG???"

    result = normalize_query(query)

    assert result == "what is rag?"


def test_normalize_repeated_exclamation_marks():
    query = "Explain RAG!!!"

    result = normalize_query(query)

    assert result == "explain rag!"


def test_normalize_clean_query():
    query = "what is rag?"

    result = normalize_query(query)

    assert result == query


def test_normalize_empty_query():
    result = normalize_query("")

    assert result == ""


def test_normalize_whitespace_only_query():
    result = normalize_query("     ")

    assert result == ""