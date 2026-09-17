from ollama import chat


MODEL = "qwen2.5-coder:7b"


def stream_response(messages):
    """
    Send conversation history to the LLM
    and stream the response.
    """

    stream = chat(
        model=MODEL,
        messages=messages,
        stream=True,
        options={
            "temperature": 0.4,
            "num_predict": 500
        }
    )

    for chunk in stream:
        content = chunk["message"]["content"]

        if content:
            yield content