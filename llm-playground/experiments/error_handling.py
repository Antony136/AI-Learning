from ollama import chat


MODEL = "qwen2.5-coder:7b"


def ask_llm(prompt: str) -> str:

    try:
        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content

    except Exception as e:
        print(f"LLM error: {e}")
        return ""

topic = input("Enter a topic: ")

answer = ask_llm(
    f"Explain {topic} to a beginner."
)

print("\nAI:")
print(answer)