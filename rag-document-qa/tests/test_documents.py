from app.storage.documents import get_documents


if __name__ == "__main__":

    documents = get_documents()

    print("\nDocuments")
    print("=" * 60)

    if not documents:
        print("No documents found.")

    for document in documents:
        print(
            f"ID: {document['id']}"
        )

        print(
            f"Filename: {document['filename']}"
        )

        print(
            f"Created: {document['created_at']}"
        )

        print(
            f"Chunks: {document['chunk_count']}"
        )

        print("-" * 60)