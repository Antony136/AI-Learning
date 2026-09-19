from app.ingestion.embeddings import generate_embedding
from experiments.retrieve_chunks import search_experiment_chunks


evaluation_data = [
    {
        "question": "What is GenAI?",
        "relevant_pages": [1]
    },
    {
        "question": "What is RAG?",
        "relevant_pages": [2]
    },
    {
        "question": "What are embeddings?",
        "relevant_pages": [4]
    },
    {
        "question": "What is a vector store?",
        "relevant_pages": [4]
    },
    {
        "question": "What is fine-tuning?",
        "relevant_pages": [2]
    },
]


CONFIGURATIONS = [
    (1000, 0),
    (1000, 1),
    (1000, 2)
]


def reciprocal_rank(results, relevant_pages):
    for rank, result in enumerate(results, start=1):
        if result["page"] in relevant_pages:
            return 1 / rank

    return 0


def evaluate_configuration(
    chunk_size,
    overlap_sentences
):
    hit_at_1 = 0
    hit_at_3 = 0
    hit_at_5 = 0

    reciprocal_ranks = []

    print()
    print("=" * 70)
    print(
        f"Chunk size: {chunk_size} | "
        f"Overlap: {overlap_sentences}"
    )
    print("=" * 70)

    for item in evaluation_data:

        question = item["question"]
        relevant_pages = item["relevant_pages"]

        query_embedding = generate_embedding(
            question
        )

        results = search_experiment_chunks(
            query_embedding=query_embedding,
            chunk_size=chunk_size,
            overlap_sentences=overlap_sentences,
            top_k=5
        )

        pages = [
            result["page"]
            for result in results
        ]

        rr = reciprocal_rank(
            results,
            relevant_pages
        )

        reciprocal_ranks.append(rr)

        if results and results[0]["page"] in relevant_pages:
            hit_at_1 += 1

        if any(
            result["page"] in relevant_pages
            for result in results[:3]
        ):
            hit_at_3 += 1

        if any(
            result["page"] in relevant_pages
            for result in results[:5]
        ):
            hit_at_5 += 1

        print()
        print(f"Question: {question}")
        print(f"Relevant pages: {relevant_pages}")
        print(f"Retrieved pages: {pages}")
        print(f"RR: {rr:.4f}")

    total = len(evaluation_data)

    print()
    print("-" * 70)

    print(
        f"Hit@1: "
        f"{hit_at_1 / total:.2%}"
    )

    print(
        f"Hit@3: "
        f"{hit_at_3 / total:.2%}"
    )

    print(
        f"Hit@5: "
        f"{hit_at_5 / total:.2%}"
    )

    print(
        f"MRR: "
        f"{sum(reciprocal_ranks) / total:.4f}"
    )


if __name__ == "__main__":

    for chunk_size, overlap in CONFIGURATIONS:

        evaluate_configuration(
            chunk_size,
            overlap
        )