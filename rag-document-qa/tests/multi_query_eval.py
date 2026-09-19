from app.ingestion.embeddings import generate_embedding
from app.retrieval.vector_store import search_similar_chunks
from app.retrieval.multi_query import multi_query_retrieve


evaluation_data = [
    {
        "question": "What is GenAI?",
        "relevant_chunks": [(1, 1)]
    },
    {
        "question": "What is RAG?",
        "relevant_chunks": [(2, 5)]
    },
    {
        "question": "What are embeddings?",
        "relevant_chunks": [(4, 1)]
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
        "relevant_chunks": [(2, 5)]
    }
]


def is_relevant(result, relevant_chunks):
    return (
        result["page"],
        result["chunk_index"]
    ) in relevant_chunks


def calculate_metrics(results, relevant_chunks):
    ranks = []

    for rank, result in enumerate(results, start=1):
        if is_relevant(result, relevant_chunks):
            ranks.append(rank)

    hit_at_1 = 1 if any(rank <= 1 for rank in ranks) else 0
    hit_at_3 = 1 if any(rank <= 3 for rank in ranks) else 0
    hit_at_5 = 1 if any(rank <= 5 for rank in ranks) else 0

    if ranks:
        reciprocal_rank = 1 / min(ranks)
    else:
        reciprocal_rank = 0.0

    return {
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "hit_at_5": hit_at_5,
        "reciprocal_rank": reciprocal_rank
    }


def single_query_retrieve(question):
    query_embedding = generate_embedding(question)

    return search_similar_chunks(
        query_embedding,
        top_k=5,
        max_distance=0.50
    )


def evaluate_method(method_name, retrieve_function):
    print("\n" + "=" * 70)
    print(method_name)
    print("=" * 70)

    total_hit_1 = 0
    total_hit_3 = 0
    total_hit_5 = 0
    total_mrr = 0.0

    for item in evaluation_data:
        question = item["question"]
        relevant_chunks = item["relevant_chunks"]

        results = retrieve_function(question)

        metrics = calculate_metrics(
            results,
            relevant_chunks
        )

        total_hit_1 += metrics["hit_at_1"]
        total_hit_3 += metrics["hit_at_3"]
        total_hit_5 += metrics["hit_at_5"]
        total_mrr += metrics["reciprocal_rank"]

        print(f"\nQuestion: {question}")

        print(
            f"Relevant chunks: "
            f"{relevant_chunks}"
        )

        print("Retrieved:")

        for rank, result in enumerate(
            results[:5],
            start=1
        ):
            marker = (
                "✓"
                if is_relevant(
                    result,
                    relevant_chunks
                )
                else " "
            )

            print(
                f"  {marker} Rank {rank}: "
                f"Page {result['page']} "
                f"Chunk {result['chunk_index']}"
            )

        print(
            f"Hit@1: {metrics['hit_at_1']} | "
            f"Hit@3: {metrics['hit_at_3']} | "
            f"Hit@5: {metrics['hit_at_5']} | "
            f"RR: {metrics['reciprocal_rank']:.4f}"
        )

    count = len(evaluation_data)

    print("\n" + "-" * 70)
    print("SUMMARY")
    print("-" * 70)

    print(
        f"Hit@1: "
        f"{total_hit_1 / count:.4f}"
    )

    print(
        f"Hit@3: "
        f"{total_hit_3 / count:.4f}"
    )

    print(
        f"Hit@5: "
        f"{total_hit_5 / count:.4f}"
    )

    print(
        f"MRR: "
        f"{total_mrr / count:.4f}"
    )


if __name__ == "__main__":

    evaluate_method(
        "SINGLE QUERY RETRIEVAL",
        single_query_retrieve
    )

    evaluate_method(
        "MULTI QUERY + RRF",
        multi_query_retrieve
    )