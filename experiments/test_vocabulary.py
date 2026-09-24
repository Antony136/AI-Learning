from app.retrieval.vocabulary import get_document_vocabulary
from app.retrieval.query_correction import correct_query


DOCUMENT_ID = 3

QUERIES = [
    "What are the applications of Differtial Calculus?",
    "What are the applications of Differntial Calculus?",
    "What are the applications of differental Calculus?",
    "What is RAG?",
    "What is pgvector?",
    "Explain FastAPI",
    "What are embeddings?"
]


vocabulary = get_document_vocabulary(DOCUMENT_ID)

print("=" * 70)
print(f"Document vocabulary size: {len(vocabulary)}")
print("=" * 70)


for query in QUERIES:

    corrected_query, corrections = correct_query(
        query,
        vocabulary,
        similarity_threshold=0.90
    )

    print("\n" + "-" * 70)
    print(f"ORIGINAL : {query}")
    print(f"CORRECTED: {corrected_query}")

    if corrections:
        print("CORRECTIONS:")

        for correction in corrections:
            print(
                f"  {correction['original']} "
                f"-> {correction['corrected']} "
                f"(similarity={correction['score']:.4f}, "
                f"edit_distance={correction['edit_distance']})"
            )
    else:
        print("CORRECTIONS: None")