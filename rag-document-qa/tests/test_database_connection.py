from app.core.database import get_connection


def test_database_is_test_database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            database_name = cursor.fetchone()[0]

        assert database_name == "rag_document_qa_test"

    finally:
        connection.close()