import re

from app.core.database import get_connection


def get_document_vocabulary(document_ids=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if document_ids is not None:

                if not document_ids:
                    return set()

                placeholders = ", ".join(
                    ["%s"] * len(document_ids)
                )

                query = f"""
                    SELECT content
                    FROM document_chunks
                    WHERE document_id IN ({placeholders})
                """

                cursor.execute(
                    query,
                    document_ids
                )

            else:

                cursor.execute(
                    """
                    SELECT content
                    FROM document_chunks
                    """
                )

            rows = cursor.fetchall()

        vocabulary = set()

        for row in rows:

            text = row[0]

            words = re.findall(
                r"\b[A-Za-z][A-Za-z-]{2,}\b",
                text
            )

            for word in words:
                vocabulary.add(word.lower())

        return vocabulary

    finally:
        connection.close()