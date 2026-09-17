from app.llm import MODEL, stream_response


SYSTEM_PROMPT = """
You are a helpful programming assistant.

Explain programming concepts clearly.
Prefer simple explanations and practical examples.
Do not unnecessarily overcomplicate your answers.
"""


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def show_history():
    print("\n--- Conversation History ---")

    for message in messages:
        role = message["role"]

        if role == "system":
            continue

        print(f"{role}: {message['content'][:200]}")

    print("-----------------------------\n")


def main():

    print("=" * 50)
    print("        LLM Playground")
    print("        Model:", MODEL)
    print("=" * 50)

    print("""
Commands:
  /clear    Clear conversation
  /history  Show conversation history
  /model    Show current model
  /exit     Exit
""")

    while True:

        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        # Exit
        if user_input.lower() == "/exit":
            print("Goodbye!")
            break

        # Clear history
        if user_input.lower() == "/clear":

            messages.clear()

            messages.append(
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            )

            print("Conversation cleared.")
            continue

        # Show history
        if user_input.lower() == "/history":
            show_history()
            continue

        # Show model
        if user_input.lower() == "/model":
            print(f"Current model: {MODEL}")
            continue

        # Add user message
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        print("\nAI: ", end="", flush=True)

        assistant_response = ""

        try:

            for text in stream_response(messages):

                print(text, end="", flush=True)

                assistant_response += text

            print()

            # Save AI response
            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_response
                }
            )

        except Exception as e:

            print(f"\nLLM error: {e}")

            # Remove failed user message
            messages.pop()


if __name__ == "__main__":
    main()