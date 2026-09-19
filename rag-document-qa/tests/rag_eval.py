from app.rag import answer_question


evaluation_data = [
    {
        "question": "What is GenAI?",
    },
    {
        "question": "What is RAG?",
    },
    {
        "question": "What are embeddings?",
    },
    {
        "question": "What is a vector store?",
    },
    {
        "question": "What is fine-tuning?",
    },
]


def evaluate_grounding(answer, results):
    if not results:
        return 0.0

    context = " ".join(
        result["content"]
        for result in results
    ).lower()

    answer_words = [
        word.strip(".,!?;:()[]\"'")
        for word in answer.lower().split()
    ]

    meaningful_words = [
        word
        for word in answer_words
        if len(word) >= 5
    ]

    if not meaningful_words:
        return 0.0

    supported_words = [
        word
        for word in meaningful_words
        if word in context
    ]

    return (
        len(supported_words)
        / len(meaningful_words)
    )


def main():

    grounding_scores = []

    print("=" * 70)
    print("RAG GROUNDEDNESS EVALUATION")
    print("=" * 70)

    for item in evaluation_data:

        question = item["question"]

        print()
        print("-" * 70)
        print(f"Question: {question}")

        answer, results = answer_question(
            question,
            retrieval_top_k=10,
            final_top_n=5,
            max_distance=0.50
        )

        grounding_score = evaluate_grounding(
            answer,
            results
        )

        grounding_scores.append(
            grounding_score
        )

        print()
        print("Answer:")
        print(answer)

        print()
        print(
            f"Retrieved chunks: "
            f"{len(results)}"
        )

        print(
            f"Grounding score: "
            f"{grounding_score:.2%}"
        )

    average_score = (
        sum(grounding_scores)
        / len(grounding_scores)
    )

    print()
    print("=" * 70)
    print(
        f"Average grounding score: "
        f"{average_score:.2%}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()