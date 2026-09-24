from app.generation.llm import generate_answer_stream


context = """
Retrieval-Augmented Generation (RAG) combines information retrieval
with text generation. A RAG system first retrieves relevant information
from a knowledge source and then provides that information to a language
model so that it can generate a grounded answer.
"""


for chunk in generate_answer_stream(
    "What is RAG?",
    context
):
    print(chunk, end="", flush=True)

print()