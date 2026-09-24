from ollama import chat


MODEL = "qwen2.5-coder:7b"


def rewrite_query(query: str):
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a search query rewriting assistant.\n\n"
                    "Rewrite the user's question into a clear search query "
                    "for a document retrieval system.\n\n"
                    "Rules:\n"
                    "1. Preserve the original meaning.\n"
                    "2. Correct obvious spelling mistakes.\n"
                    "3. Do not add information that is not present in the question.\n"
                    "4. Preserve technical terms such as RAG, LLM, FastAPI, "
                    "pgvector, Qwen, PostgreSQL, React and similar terms.\n"
                    "5. Return ONLY the rewritten query.\n"
                    "6. Do not explain your changes."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],
        options={
            "temperature": 0.0,
            "num_predict": 100
        }
    )

    return response.message.content.strip()