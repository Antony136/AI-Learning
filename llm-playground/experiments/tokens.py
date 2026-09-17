from ollama import chat

def explanation_prompt(topic):
    return f"""
You are a programming tutor.

Explain the following topic to a beginner:

Topic: {topic}

Your response should contain:

1. Simple explanation
2. Real-world analogy
3. Code example
4. Common mistake

Keep the explanation concise.
"""

while True:
    topic = input("\nEnter a topic (or 'exit' to quit): ")

    if topic.lower() == "exit":
        break

    prompt = explanation_prompt(topic)

    response = chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nAI:")
    print(response.message.content)

    print("\nToken information:")
    print("Input tokens:", response.prompt_eval_count)
    print("Output tokens:", response.eval_count)