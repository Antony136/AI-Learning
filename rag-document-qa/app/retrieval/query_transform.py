from ollama import chat


MODEL = "qwen2.5-coder:7b"


def generate_queries(
    question: str,
    num_queries: int = 3
):
    prompt = f"""
You are helping a document retrieval system.

Generate {num_queries} different search queries for the user's question.

Requirements:
- Preserve the meaning of the original question.
- Use different wording for each query.
- Explore different aspects or formulations of the same information need.
- Use important technical terms when appropriate.
- Do not answer the question.
- Do not number the queries.
- Return ONLY the queries.
- Put exactly one query on each line.

User question:
{question}
"""

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.5,
            "num_predict": 200
        }
    )

    queries = [
        line.strip()
        for line in response.message.content.splitlines()
        if line.strip()
    ]

    return queries[:num_queries]