from ollama import chat


stream = chat(
    model="qwen2.5-coder:7b",
    messages=[
        {
            "role": "user",
            "content": "Explain how FastAPI works in detail."
        }
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

print()