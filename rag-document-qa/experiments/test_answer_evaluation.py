from experiments.evaluation_answers import evaluation_answers
from app.rag import answer_question
from app.evaluation.grounding import evaluate_claim


DOCUMENT_ID = 2


def build_context(results):
    return "\n\n".join(
        result["content"]
        for result in results
    )


def evaluate_answers():

    total_claims = 0
    supported_claims = 0
    unsupported_claims = 0
    invalid_evaluations = 0

    print("\n" + "=" * 70)
    print("RAG SEMANTIC ANSWER EVALUATION")
    print("=" * 70)

    for index, item in enumerate(
        evaluation_answers,
        start=1
    ):

        question = item["question"]
        reference_answer = item["reference_answer"]
        expected_claims = item["expected_claims"]

        print("\n" + "-" * 70)
        print(f"Question {index}: {question}")

        answer, results = answer_question(
            question=question,
            document_ids=[DOCUMENT_ID]
        )

        context = build_context(results)

        print("\nReference answer:")
        print(reference_answer)

        print("\nGenerated answer:")
        print(answer)

        print("\nSemantic grounding evaluation:")

        for claim in expected_claims:

            result = evaluate_claim(
                claim=claim,
                context=context
            )

            verdict = result["verdict"]
            reason = result["reason"]

            total_claims += 1

            if verdict == "SUPPORTED":
                supported_claims += 1

            elif verdict == "NOT_SUPPORTED":
                unsupported_claims += 1

            elif verdict == "INVALID":
                invalid_evaluations += 1

            print("\nClaim:")
            print(claim)

            print("\nVerdict:")
            print(verdict)

            print("\nReason:")
            print(reason)

        print("\nRetrieved sources:")

        for rank, result in enumerate(
            results,
            start=1
        ):
            print(
                f"Rank {rank}: "
                f"Page {result['page']} | "
                f"Chunk {result['chunk_index']} | "
                f"Score {result['rerank_score']:.4f}"
            )

    print("\n" + "=" * 70)
    print("SEMANTIC EVALUATION SUMMARY")
    print("=" * 70)

    grounding_score = (
        supported_claims / total_claims
        if total_claims > 0
        else 0
    )

    print(
        f"Total claims evaluated: "
        f"{total_claims}"
    )

    print(
        f"Supported claims: "
        f"{supported_claims}"
    )

    print(
        f"Unsupported claims: "
        f"{unsupported_claims}"
    )

    print(
        f"Invalid evaluations: "
        f"{invalid_evaluations}"
    )

    print(
        f"Grounding score: "
        f"{grounding_score:.2%}"
    )


if __name__ == "__main__":
    evaluate_answers()