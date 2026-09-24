from app.retrieval.search import retrieve


evaluation_data = [
    {
        "question": "What is GenAI?",
        "relevant_chunks": [
            (1, 1)
        ]
    },
    {
        "question": "What is RAG?",
        "relevant_chunks": [
            (2, 5)
        ]
    },
    {
        "question": "What are embeddings?",
        "relevant_chunks": [
            (4, 1)
        ]
    },
    {
        "question": "What is a vector store?",
        "relevant_chunks": [
            (4, 2),
            (4, 3),
            (4, 4)
        ]
    },
    {
        "question": "What is fine-tuning?",
        "relevant_chunks": [
            (2, 5)
        ]
    }
]


def is_relevant(result, relevant_chunks):
    return (
        result["page"],
        result["chunk_index"]
    ) in relevant_chunks


def hit_at_k(results, relevant_chunks, k):
    top_results = results[:k]

    return any(
        is_relevant(result, relevant_chunks)
        for result in top_results
    )


def reciprocal_rank(results, relevant_chunks):
    for rank, result in enumerate(results, start=1):

        if is_relevant(result, relevant_chunks):
            return 1 / rank

    return 0


if __name__ == "__main__":

    print("=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)

    reciprocal_ranks = []

    for item in evaluation_data:

        question = item["question"]
        relevant_chunks = item["relevant_chunks"]

        results = retrieve(
            question,
            top_k=10,
            max_distance=0.50
        )

        print("\n")
        print("-" * 80)
        print(f"Question: {question}")
        print(f"Expected: {relevant_chunks}")

        print("\nRetrieved:")

        for rank, result in enumerate(
            results,
            start=1
        ):
            print(
                f"{rank}. "
                f"Page {result['page']} "
                f"Chunk {result['chunk_index']} "
                f"Distance {result['distance']:.4f}"
            )

        hit1 = hit_at_k(
            results,
            relevant_chunks,
            1
        )

        hit3 = hit_at_k(
            results,
            relevant_chunks,
            3
        )

        hit5 = hit_at_k(
            results,
            relevant_chunks,
            5
        )

        rr = reciprocal_rank(
            results,
            relevant_chunks
        )

        reciprocal_ranks.append(rr)

        print("\nMetrics:")
        print(f"Hit@1: {'YES' if hit1 else 'NO'}")
        print(f"Hit@3: {'YES' if hit3 else 'NO'}")
        print(f"Hit@5: {'YES' if hit5 else 'NO'}")
        print(f"Reciprocal Rank: {rr:.4f}")

    print("\n")
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total = len(evaluation_data)

    hit1_total = sum(
        hit_at_k(
            retrieve(
                item["question"],
                top_k=10,
                max_distance=0.50
            ),
            item["relevant_chunks"],
            1
        )
        for item in evaluation_data
    )

    hit3_total = sum(
        hit_at_k(
            retrieve(
                item["question"],
                top_k=10,
                max_distance=0.50
            ),
            item["relevant_chunks"],
            3
        )
        for item in evaluation_data
    )

    hit5_total = sum(
        hit_at_k(
            retrieve(
                item["question"],
                top_k=10,
                max_distance=0.50
            ),
            item["relevant_chunks"],
            5
        )
        for item in evaluation_data
    )

    print(f"Hit@1: {hit1_total / total:.2%}")
    print(f"Hit@3: {hit3_total / total:.2%}")
    print(f"Hit@5: {hit5_total / total:.2%}")

    mrr = sum(reciprocal_ranks) / len(
        reciprocal_ranks
    )

    print(f"MRR:    {mrr:.4f}")