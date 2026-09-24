from app.retrieval.search import retrieve
from app.retrieval.reranker import rerank
from app.retrieval.query_correction import correct_query
from app.retrieval.vocabulary import get_document_vocabulary


DOCUMENT_ID = 3

QUERIES = [
    "What are the applications of Differtial Calculus?",
    "What are the applications of Differntial Calculus?",
    "What are the applications of differental Calculus?",
    "What are embeddings?",
    "What is pgvector?",
    "What is RAG?"
]


def evaluate_query(query: str):
    """
    Run the complete retrieval + reranking process
    for a query.
    """

    results = retrieve(
        question=query,
        top_k=10,
        max_distance=0.50,
        document_id=DOCUMENT_ID
    )

    reranked = rerank(
        question=query,
        results=results,
        top_n=5
    )

    if not reranked:
        return {
            "best_score": None,
            "best_result": None
        }

    return {
        "best_score": reranked[0]["rerank_score"],
        "best_result": reranked[0]
    }


vocabulary = get_document_vocabulary(DOCUMENT_ID)


for original_query in QUERIES:

    corrected_query, corrections = correct_query(
        original_query,
        vocabulary,
        similarity_threshold=0.90,
        max_edit_distance=2
    )

    print("\n" + "=" * 90)
    print(f"ORIGINAL QUERY : {original_query}")
    print(f"CANDIDATE QUERY: {corrected_query}")
    print("=" * 90)

    if corrections:
        print("\nCandidate correction:")
        for correction in corrections:
            print(
                f"  {correction['original']} "
                f"-> {correction['corrected']} "
                f"(similarity={correction['score']:.4f}, "
                f"edit_distance={correction['edit_distance']})"
            )
    else:
        print("\nNo correction candidate generated.")

    print("\nEvaluating ORIGINAL query...")

    original_result = evaluate_query(
        original_query
    )

    print(
        f"Best reranker score: "
        f"{original_result['best_score']}"
    )

    if original_result["best_result"]:
        result = original_result["best_result"]

        print(
            f"Best result: "
            f"Page {result['page']} "
            f"Chunk {result['chunk_index']}"
        )

    if corrected_query == original_query:
        print("\nNo candidate correction.")
        continue

    print("\nEvaluating CANDIDATE query...")

    corrected_result = evaluate_query(
        corrected_query
    )

    print(
        f"Best reranker score: "
        f"{corrected_result['best_score']}"
    )

    if corrected_result["best_result"]:
        result = corrected_result["best_result"]

        print(
            f"Best result: "
            f"Page {result['page']} "
            f"Chunk {result['chunk_index']}"
        )

    if (
        original_result["best_score"] is not None
        and corrected_result["best_score"] is not None
    ):
        improvement = (
            corrected_result["best_score"]
            - original_result["best_score"]
        )

        print(
            f"\nRERANKER SCORE CHANGE: "
            f"{improvement:+.4f}"
        )

        if improvement > 0:
            print("Candidate improved the reranker score.")
        else:
            print("Candidate did NOT improve the reranker score.")