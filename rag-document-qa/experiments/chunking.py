import re


def split_into_sentences(text: str):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def chunk_text(
    text: str,
    chunk_size: int,
    overlap_sentences: int
):
    sentences = split_into_sentences(text)

    chunks = []
    current_sentences = []

    for sentence in sentences:

        current_text = " ".join(
            current_sentences
        )

        if (
            current_sentences
            and len(current_text)
            + len(sentence)
            + 1
            > chunk_size
        ):
            chunks.append(current_text)

            if overlap_sentences > 0:
                overlap = current_sentences[
                    -overlap_sentences:
                ]
            else:
                overlap = []

            current_sentences = (
                overlap + [sentence]
            )

        else:
            current_sentences.append(
                sentence
            )

    if current_sentences:
        chunks.append(
            " ".join(current_sentences)
        )

    return chunks