from app.retrieval.search import retrieve
from app.generation.prompts import build_context
from app.generation.llm import generate_answer


def answer_question(question: str, top_k: int = 5):
    results = retrieve(
        question,
        top_k=top_k
    )

    context = build_context(results)

    answer = generate_answer(
        question,
        context
    )

    return answer, results


if __name__ == "__main__":
    question = input("Question: ")

    answer, results = answer_question(question)

    print("\nAnswer:")
    print("=" * 70)
    print(answer)

    print("\nSources:")
    print("=" * 70)

    for result in results:
        print(
            f"- {result['source']} "
            f"(Page {result['page']}, "
            f"Chunk {result['chunk_index']})"
        )