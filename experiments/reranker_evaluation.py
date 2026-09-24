from app.retrieval.search import retrieve
from app.retrieval.reranker import rerank


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


def reciprocal_rank(results, relevant_chunks):
    for rank, result in enumerate(results, start=1):

        if is_relevant(result, relevant_chunks):
            return 1 / rank

    return 0


if __name__ == "__main__":

    vector_rr = []
    reranked_rr = []

    print("=" * 80)
    print("VECTOR SEARCH vs RERANKING")
    print("=" * 80)

    for item in evaluation_data:

        question = item["question"]
        relevant_chunks = item["relevant_chunks"]

        results = retrieve(
            question,
            top_k=10,
            max_distance=0.50
        )

        reranked_results = rerank(
            question,
            results,
            top_n=5
        )

        vector_rank = reciprocal_rank(
            results,
            relevant_chunks
        )

        reranked_rank = reciprocal_rank(
            reranked_results,
            relevant_chunks
        )

        vector_rr.append(vector_rank)
        reranked_rr.append(reranked_rank)

        print("\n")
        print("-" * 80)
        print(f"Question: {question}")

        print("\nVECTOR SEARCH")
        print("-" * 80)

        for rank, result in enumerate(
            results[:5],
            start=1
        ):
            relevant = is_relevant(
                result,
                relevant_chunks
            )

            marker = "YES" if relevant else "NO"

            print(
                f"{rank}. "
                f"Page {result['page']} "
                f"Chunk {result['chunk_index']} "
                f"Relevant: {marker} "
                f"Distance: {result['distance']:.4f}"
            )

        print("\nRERANKED")
        print("-" * 80)

        for rank, result in enumerate(
            reranked_results,
            start=1
        ):
            relevant = is_relevant(
                result,
                relevant_chunks
            )

            marker = "YES" if relevant else "NO"

            print(
                f"{rank}. "
                f"Page {result['page']} "
                f"Chunk {result['chunk_index']} "
                f"Relevant: {marker} "
                f"Score: {result['rerank_score']:.4f}"
            )

        print("\nReciprocal Rank")
        print("-" * 80)

        print(
            f"Vector Search: {vector_rank:.4f}"
        )

        print(
            f"Reranked:      {reranked_rank:.4f}"
        )

    print("\n")
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    vector_mrr = sum(vector_rr) / len(vector_rr)
    reranked_mrr = sum(reranked_rr) / len(reranked_rr)

    print(
        f"Vector Search MRR: {vector_mrr:.4f}"
    )

    print(
        f"Reranked MRR:      {reranked_mrr:.4f}"
    )