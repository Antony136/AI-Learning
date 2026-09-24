from ollama import chat


MODEL = "qwen2.5-coder:7b"


def build_messages(question: str, context: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a document question-answering assistant. "
                "Answer the user's question using only the provided context. "
                "Do not use outside knowledge. "
                "If the answer is not present in the context, "
                "say that you could not find the answer in the document.\n\n"

                "When the context contains enough information, "
                "give a clear and useful explanation. "
                "For definition questions, include the definition "
                "and briefly explain how it works. "
                "Use short paragraphs or bullet points when helpful. "
                "Do not unnecessarily repeat information."
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n\n"
                f"{context}\n\n"
                f"Question:\n"
                f"{question}"
            )
        }
    ]


def generate_answer(question: str, context: str):
    messages = build_messages(
        question,
        context
    )

    response = chat(
        model=MODEL,
        messages=messages,
        options={
            "temperature": 0.2,
            "num_predict": 500
        }
    )

    return response.message.content


def generate_answer_stream(question: str, context: str):
    messages = build_messages(
        question,
        context
    )

    stream = chat(
        model=MODEL,
        messages=messages,
        options={
            "temperature": 0.2,
            "num_predict": 500
        },
        stream=True
    )

    for chunk in stream:
        content = chunk.message.content

        if content:
            yield content