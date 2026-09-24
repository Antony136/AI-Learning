from ollama import embed

from app.core.database import get_connection
from app.storage.chunks import create_document, insert_chunk


EMBEDDING_MODEL = "nomic-embed-text"


def test_insert_chunk():
    document_id = create_document(
        "pytest_chunk_document.pdf"
    )

    content = (
        "RAG retrieves relevant information "
        "before generating an answer."
    )

    response = embed(
        model=EMBEDDING_MODEL,
        input=content
    )

    embedding = response.embeddings[0]

    insert_chunk(
        document_id=document_id,
        source="pytest_chunk_document.pdf",
        page=1,
        chunk_index=1,
        content=content,
        embedding=embedding
    )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    document_id,
                    source,
                    page,
                    chunk_index,
                    content,
                    embedding
                FROM document_chunks
                WHERE document_id = %s
                """,
                (document_id,)
            )

            row = cursor.fetchone()

        assert row is not None

        assert row[1] == document_id
        assert row[2] == "pytest_chunk_document.pdf"
        assert row[3] == 1
        assert row[4] == 1
        assert row[5] == content
        assert row[6] is not None

    finally:
        connection.close()


def test_document_chunk_relationship():
    document_id = create_document(
        "pytest_relationship_document.pdf"
    )

    contents = [
        "First chunk of the document.",
        "Second chunk of the document.",
    ]

    for chunk_index, content in enumerate(contents, start=1):
        response = embed(
            model=EMBEDDING_MODEL,
            input=content
        )

        embedding = response.embeddings[0]

        insert_chunk(
            document_id=document_id,
            source="pytest_relationship_document.pdf",
            page=1,
            chunk_index=chunk_index,
            content=content,
            embedding=embedding
        )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*)
                FROM document_chunks
                WHERE document_id = %s
                """,
                (document_id,)
            )

            chunk_count = cursor.fetchone()[0]

        assert chunk_count == 2

    finally:
        connection.close()

def test_delete_document_cascades_to_chunks():
    document_id = create_document(
        "pytest_cascade_document.pdf"
    )

    contents = [
        "First chunk for cascade testing.",
        "Second chunk for cascade testing.",
        "Third chunk for cascade testing.",
    ]

    for chunk_index, content in enumerate(contents, start=1):
        response = embed(
            model=EMBEDDING_MODEL,
            input=content
        )

        embedding = response.embeddings[0]

        insert_chunk(
            document_id=document_id,
            source="pytest_cascade_document.pdf",
            page=1,
            chunk_index=chunk_index,
            content=content,
            embedding=embedding
        )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Verify chunks exist
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM document_chunks
                WHERE document_id = %s
                """,
                (document_id,)
            )

            chunk_count_before = cursor.fetchone()[0]

            assert chunk_count_before == 3

            # Delete the document
            cursor.execute(
                """
                DELETE FROM documents
                WHERE id = %s
                """,
                (document_id,)
            )

        connection.commit()

    finally:
        connection.close()

    # Verify chunks were automatically deleted
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM document_chunks
                WHERE document_id = %s
                """,
                (document_id,)
            )

            chunk_count_after = cursor.fetchone()[0]

            assert chunk_count_after == 0

    finally:
        connection.close()