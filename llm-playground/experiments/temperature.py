from ollama import chat

prompt = """
Give me one creative name for an AI-powered developer productivity application.
Return only the name.
"""

temperatures = [0.0, 0.3, 0.5, 0.7, 1.0]

for temperature in temperatures:

    response = chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": temperature
        }
    )

    print("=" * 60)
    print(f"Temperature: {temperature}")
    print("=" * 60)
    print(response.message.content)