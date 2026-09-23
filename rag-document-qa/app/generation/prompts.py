def build_context(results):
    parts = []

    for result in results:
        parts.append(
            f"[Source: {result['source']}, "
            f"Page: {result['page']}, "
            f"Chunk: {result['chunk_index']}]\n"
            f"{result['content']}"
        )

    return "\n\n".join(parts)

def build_question_rewrite_prompt(
    question: str,
    conversation: list[dict]
):
    conversation_text = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in conversation
    )

    return f"""
You are a query rewriting assistant for a RAG system.

Your job is to rewrite the user's latest question into a
standalone question that can be understood without the conversation.

Rules:
- Preserve the original meaning.
- Resolve references such as "it", "they", "this", "that", etc.
- Use previous conversation only when necessary.
- Do not answer the question.
- Return ONLY the rewritten question.

Conversation:
{conversation_text}

Latest question:
{question}

Standalone question:
""".strip()