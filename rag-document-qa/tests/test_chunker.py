from app.ingestion.chunker import chunk_text


text = """
Retrieval-Augmented Generation combines
information retrieval with language-model generation.

The system first retrieves relevant information.
That information is then provided to the language model.

The model uses the retrieved information
to generate a grounded answer.
"""


chunks = chunk_text(
    text,
    chunk_size=150,
    overlap_sentences=1
)


print("Number of chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print("\n" + "=" * 60)
    print(f"CHUNK {index}")
    print("=" * 60)
    print(chunk)