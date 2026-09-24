from experiments.evaluation_dataset import evaluation_dataset
from app.retrieval.multi_query import multi_query_retrieve
from app.retrieval.reranker import rerank

DOCUMENT_ID = 2


def is_relevant(result, relevant_chunks):
    for expected in relevant_chunks:
        if (
            result["document_id"] == expected["document_id"]
            and result["page"] == expected["page"]
            and result["chunk_index"] == expected["chunk"]
        ):
            return True

    return False

def find_relevant_rank(results, relevant_chunks):
    for rank, result in enumerate(
        results,
        start=1
    ):
        if is_relevant(
            result,
            relevant_chunks
        ):
            return rank

    return None

def evaluate_recall_at_k(results, relevant_chunks, k):
    top_results = results[:k]

    for result in top_results:
        if is_relevant(result, relevant_chunks):
            return True

    return False


def evaluate_retrieval():
    total_questions = len(evaluation_dataset)

    recall_at_1 = 0
    recall_at_3 = 0
    recall_at_5 = 0

    rrf_reciprocal_ranks = []
    reranker_reciprocal_ranks = []

    print("\n" + "=" * 70)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 70)

    for index, item in enumerate(
        evaluation_dataset,
        start=1
    ):
        question = item["question"]
        relevant_chunks = item["relevant_chunks"]

        print("\n" + "-" * 70)
        print(f"Question {index}: {question}")

        print("\nExpected relevant chunks:")

        for expected in relevant_chunks:
            print(
                f"Document {expected['document_id']} | "
                f"Page {expected['page']} | "
                f"Chunk {expected['chunk']}"
            )

        results = multi_query_retrieve(
            question=question,
            num_queries=3,
            top_k_per_query=5,
            document_ids=[DOCUMENT_ID]
        )

        print("\nRetrieved chunks:")

        for rank, result in enumerate(
            results[:5],
            start=1
        ):
            print(
                f"Rank {rank}: "
                f"Page {result['page']} | "
                f"Chunk {result['chunk_index']} | "
                f"RRF {result['rrf_score']:.6f}"
            )

        hit_at_1 = evaluate_recall_at_k(
            results,
            relevant_chunks,
            1
        )

        hit_at_3 = evaluate_recall_at_k(
            results,
            relevant_chunks,
            3
        )

        hit_at_5 = evaluate_recall_at_k(
            results,
            relevant_chunks,
            5
        )

        rrf_rank = find_relevant_rank(
            results,
            relevant_chunks
        )

        reranked_results = rerank(
            question,
            results,
            top_n=5
        )

        print("\nReranked chunks:")

        for rank, result in enumerate(
            reranked_results,
            start=1
        ):
            print(
                f"Rank {rank}: "
                f"Page {result['page']} | "
                f"Chunk {result['chunk_index']} | "
                f"Rerank {result['rerank_score']:.4f} | "
                f"RRF {result['rrf_score']:.6f}"
            )

        reranker_rank = find_relevant_rank(
            reranked_results,
            relevant_chunks
        )

        if rrf_rank is not None:
            rrf_reciprocal_ranks.append(
                1 / rrf_rank
            )

        if reranker_rank is not None:
            reranker_reciprocal_ranks.append(
                1 / reranker_rank
            )

        print(
            f"\nRRF relevant rank: "
            f"{rrf_rank if rrf_rank is not None else 'NOT FOUND'}"
        )

        print(
            f"Reranker relevant rank: "
            f"{reranker_rank if reranker_rank is not None else 'NOT FOUND'}"
        )

        if hit_at_1:
            recall_at_1 += 1

        if hit_at_3:
            recall_at_3 += 1

        if hit_at_5:
            recall_at_5 += 1

        print(
            f"\nHit@1: {'PASS' if hit_at_1 else 'FAIL'}"
        )

        print(
            f"Hit@3: {'PASS' if hit_at_3 else 'FAIL'}"
        )

        print(
            f"Hit@5: {'PASS' if hit_at_5 else 'FAIL'}"
        )

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Recall@1: "
        f"{recall_at_1 / total_questions:.2%}"
    )

    print(
        f"Recall@3: "
        f"{recall_at_3 / total_questions:.2%}"
    )

    print(
        f"Recall@5: "
        f"{recall_at_5 / total_questions:.2%}"
    )

    rrf_mrr = (
        sum(rrf_reciprocal_ranks)
        / total_questions
        if total_questions > 0
        else 0
    )

    reranker_mrr = (
        sum(reranker_reciprocal_ranks)
        / total_questions
        if total_questions > 0
        else 0
    )

    print(
        f"RRF MRR: "
        f"{rrf_mrr:.3f}"
    )

    print(
        f"Reranker MRR: "
        f"{reranker_mrr:.3f}"
    )


if __name__ == "__main__":
    evaluate_retrieval()