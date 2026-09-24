evaluation_answers = [
    {
        "question": "What is RAG?",
        "reference_answer": (
            "RAG stands for Retrieval-Augmented Generation. "
            "It combines information retrieval with text generation "
            "so that a language model can use retrieved information "
            "when generating an answer."
        ),
        "expected_claims": [
            "RAG stands for Retrieval-Augmented Generation.",
            "RAG combines information retrieval with text generation.",
            "RAG allows a language model to use retrieved information."
        ]
    },
    {
        "question": "How does RAG work?",
        "reference_answer": (
            "RAG first retrieves relevant information from a knowledge "
            "source and then provides that retrieved information to a "
            "language model, which uses it to generate the answer."
        ),
        "expected_claims": [
            "RAG retrieves relevant information.",
            "The retrieved information is provided to the language model.",
            "The language model uses the retrieved information to generate the answer."
        ]
    },
    {
        "question": "What is the purpose of chunking?",
        "reference_answer": (
            "Chunking divides a large document into smaller pieces so "
            "that the pieces can be processed, embedded, stored, and "
            "retrieved more effectively."
        ),
        "expected_claims": [
            "Chunking divides documents into smaller pieces.",
            "Chunking creates smaller retrieval units.",
            "Chunking makes retrieval more focused or efficient."
        ]
    },
    {
        "question": "What is reranking?",
        "reference_answer": (
            "Reranking is the process of reordering retrieved search "
            "results according to their relevance to the user's query."
        ),
        "expected_claims": [
            "Reranking reorders retrieved results.",
            "Reranking uses relevance to determine the new order."
        ]
    },
    {
        "question": "Why is RAG useful?",
        "reference_answer": (
            "RAG is useful because it allows a language model to use "
            "relevant retrieved information when generating answers."
        ),
        "expected_claims": [
            "RAG allows a language model to use retrieved information.",
            "Retrieved information can be used when generating answers."
        ]
    }
]