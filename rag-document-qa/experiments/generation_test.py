from app.generation.llm import generate_answer


def main():
    context = """
[Source: GenAI notes.pdf, Page: 2, Chunk: 1]
RAG stands for Retrieval-Augmented Generation.
It combines information retrieval with a language model.
The retrieval step finds relevant information from a knowledge source,
and the language model uses that information to generate an answer.

[Source: GenAI notes.pdf, Page: 3, Chunk: 2]
A vector database stores numerical representations called embeddings.
These embeddings allow semantically similar pieces of information
to be retrieved efficiently.
"""

    question = "What is FastAPI?"

    answer = generate_answer(
        question=question,
        context=context
    )

    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)
    print(question)

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(answer)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()