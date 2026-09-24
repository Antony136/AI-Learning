from ollama import chat

from app.generation.prompts import build_question_rewrite_prompt


LLM_MODEL = "qwen2.5-coder:7b"


def rewrite_question(
    question: str,
    conversation
):
    if not conversation:
        return question

    conversation_data = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in conversation
    ]

    prompt = build_question_rewrite_prompt(
        question,
        conversation_data
    )

    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    rewritten_question = response.message.content.strip()

    return rewritten_question
