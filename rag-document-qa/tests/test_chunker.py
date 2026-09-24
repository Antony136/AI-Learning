from app.ingestion.chunker import (
    split_into_sentences,
    chunk_text
)


def test_split_into_sentences():
    text = "RAG is useful. It retrieves information. Then it generates an answer."

    sentences = split_into_sentences(text)

    assert sentences == [
        "RAG is useful.",
        "It retrieves information.",
        "Then it generates an answer."
    ]


def test_chunk_short_text():
    text = "RAG retrieves relevant information."

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap_sentences=1
    )

    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_long_text():
    text = (
        "RAG retrieves information. "
        "The retrieved information is passed to the language model. "
        "The language model uses the context to generate an answer. "
        "This can improve the relevance of generated responses."
    )

    chunks = chunk_text(
        text,
        chunk_size=80,
        overlap_sentences=1
    )

    assert len(chunks) > 1


def test_chunk_overlap():
    text = (
        "Sentence one. "
        "Sentence two. "
        "Sentence three. "
        "Sentence four."
    )

    chunks = chunk_text(
        text,
        chunk_size=35,
        overlap_sentences=1
    )

    assert len(chunks) > 1

    # The final sentence of one chunk should
    # appear at the beginning of the next chunk.
    for previous, current in zip(chunks, chunks[1:]):
        previous_sentences = previous.split(". ")
        last_sentence = previous_sentences[-1]

        assert last_sentence.rstrip(".") in current


def test_empty_text():
    chunks = chunk_text(
        "",
        chunk_size=1000,
        overlap_sentences=1
    )

    assert chunks == []


def test_whitespace_text():
    chunks = chunk_text(
        "   ",
        chunk_size=1000,
        overlap_sentences=1
    )

    assert chunks == []