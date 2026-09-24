from app.retrieval.query_rewriter import rewrite_query


QUESTIONS = [
    "Differtial",
    "What are the applications of Differtial Calculus?",
    "What is RAG?",
    "explain FastAPI",
    "What is pgvector?",
    "What are embeddings?",
]


for question in QUESTIONS:

    rewritten = rewrite_query(question)

    print("\n" + "=" * 70)
    print(f"Original : {question}")
    print(f"Rewritten: {rewritten}")