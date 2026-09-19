from app.retrieval.search import retrieve
from app.retrieval.reranker import rerank
from app.generation.prompts import build_context
from app.generation.llm import generate_answer


RERANK_THRESHOLD = 1.0


def answer_question(
    question: str,
    retrieval_top_k: int = 10,
    final_top_n: int = 5,
    max_distance: float = 0.50
):
    # Stage 1: Vector retrieval
    results = retrieve(
        question,
        top_k=retrieval_top_k,
        max_distance=max_distance
    )

    if not results:
        return (
            "I could not find relevant information "
            "in the document.",
            []
        )

    # Stage 2: Cross-encoder reranking
    reranked_results = rerank(
        question,
        results,
        top_n=final_top_n
    )

    if not reranked_results:
        return (
            "I could not find relevant information "
            "in the document.",
            []
        )

    # Stage 3: Check whether the best result
    # is relevant enough to answer the question.
    best_score = reranked_results[0]["rerank_score"]

    if best_score < RERANK_THRESHOLD:
        return (
            "I could not find relevant information "
            "in the document.",
            []
        )

    # Stage 4: Build context
    context = build_context(
        reranked_results
    )

    # Stage 5: Generate grounded answer
    answer = generate_answer(
        question,
        context
    )

    return answer, reranked_results


if __name__ == "__main__":

    question = input("Question: ")

    answer, results = answer_question(
        question
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
                f"(Page {result['page']}, "
                f"Chunk {result['chunk_index']}) "
                f"[Rerank score: "
                f"{result['rerank_score']:.4f}]"
            )
