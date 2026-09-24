from app.storage.documents import get_documents
from app.storage.chunks import create_document
from app.core.database import get_connection


def test_create_document():
    filename = "pytest_test_document.pdf"

    document_id = create_document(filename)

    assert document_id is not None
    assert isinstance(document_id, int)

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, filename
                FROM documents
                WHERE id = %s
                """,
                (document_id,)
            )

            row = cursor.fetchone()

        assert row is not None
        assert row[0] == document_id
        assert row[1] == filename

    finally:
        connection.close()


def test_get_documents():
    filename = "pytest_retrieval_document.pdf"

    document_id = create_document(filename)

    documents = get_documents()

    assert isinstance(documents, list)

    matching_documents = [
        document
        for document in documents
        if document["id"] == document_id
    ]

    assert len(matching_documents) == 1

    document = matching_documents[0]

    assert document["filename"] == filename
    assert document["chunk_count"] == 0