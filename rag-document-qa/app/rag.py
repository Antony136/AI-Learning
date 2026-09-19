from app.retrieval.search import retrieve
from app.retrieval.reranker import rerank
from app.generation.prompts import build_context
from app.generation.llm import generate_answer


RERANK_THRESHOLD = 1.0


def answer_question(
    question: str,
    document_id: int,
    retrieval_top_k: int = 10,
    final_top_n: int = 5,
    max_distance: float = 0.50
):
    results = retrieve(
        question,
        top_k=retrieval_top_k,
        max_distance=max_distance,
        document_id=document_id
    )

    print("\n" + "=" * 70)
    print("VECTOR SEARCH RESULTS")
    print("=" * 70)

    if not results:
        print("NO VECTOR RESULTS")
        print(
            f"All results were filtered by "
            f"max_distance = {max_distance}"
        )

        return (
            "I could not find relevant information "
            "in the selected document.",
            []
        )

    for index, result in enumerate(
        results,
        start=1
    ):
        print(
            f"\nResult {index}"
        )

        print(
            f"Distance: "
            f"{result['distance']:.4f}"
        )

        print(
            f"Page: "
            f"{result['page']}"
        )

        print(
            f"Chunk: "
            f"{result['chunk_index']}"
        )

    reranked_results = rerank(
        question,
        results,
        top_n=final_top_n
    )

    print("\n" + "=" * 70)
    print("RERANKER RESULTS")
    print("=" * 70)

    for index, result in enumerate(
        reranked_results,
        start=1
    ):
        print(
            f"\nResult {index}"
        )

        print(
            f"Rerank score: "
            f"{result['rerank_score']:.4f}"
        )

        print(
            f"Vector distance: "
            f"{result['distance']:.4f}"
        )

        print(
            f"Page: "
            f"{result['page']}"
        )

        print(
            f"Chunk: "
            f"{result['chunk_index']}"
        )

    if not reranked_results:
        return (
            "I could not find relevant information "
            "in the selected document.",
            []
        )

    best_score = reranked_results[0]["rerank_score"]

    print("\n" + "=" * 70)
    print("THRESHOLD CHECK")
    print("=" * 70)

    print(
        f"Best rerank score: {best_score:.4f}"
    )

    print(
        f"Required rerank score: "
        f"{RERANK_THRESHOLD:.4f}"
    )

    print(
        f"Passes threshold: "
        f"{best_score >= RERANK_THRESHOLD}"
    )

    if best_score < RERANK_THRESHOLD:
        print("RESULT REJECTED BY RERANKER")

        return (
            "I could not find relevant information "
            "in the selected document.",
            []
        )

    context = build_context(
        reranked_results
    )

    answer = generate_answer(
        question,
        context
    )

    return answer, reranked_results

if __name__ == "__main__":

    document_id = int(
        input("Document ID: ")
    )

    question = input(
        "Question: "
    )

    answer, results = answer_question(
        question=question,
        document_id=document_id
    )

    print("\nAnswer:")
    print("=" * 70)
    print(answer)

    if results:

        print("\nSources:")
        print("=" * 70)

        for result in results:

            print(
                f"- {result['source']} "
                f"| Page {result['page']} "
                f"| Chunk {result['chunk_index']}"
            )