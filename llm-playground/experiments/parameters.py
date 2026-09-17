from ollama import chat


prompt = """
Explain what an API is to a beginner.
Use a simple real-world analogy.
"""


settings = [
    {
        "temperature": 0.0,
        "num_predict": 100
    },
    {
        "temperature": 0.7,
        "num_predict": 100
    },
    {
        "temperature": 0.7,
        "num_predict": 300
    }
]


for options in settings:

    print("\n" + "=" * 60)
    print("Options:", options)
    print("=" * 60)

    response = chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options=options
    )

    print(response.message.content)