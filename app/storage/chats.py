from app.core.database import get_connection


def create_chat_session(
    title: str = "New Chat"
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO chat_sessions (title)
                VALUES (%s)
                RETURNING id, title, created_at
                """,
                (title,)
            )

            session = cursor.fetchone()

        connection.commit()

        return {
            "id": session[0],
            "title": session[1],
            "created_at": session[2]
        }

    finally:
        connection.close()


def get_chat_session(
    session_id: int
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, title, created_at
                FROM chat_sessions
                WHERE id = %s
                """,
                (session_id,)
            )

            session = cursor.fetchone()

        if session is None:
            return None

        return {
            "id": session[0],
            "title": session[1],
            "created_at": session[2]
        }

    finally:
        connection.close()

def get_chat_sessions():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, created_at
                FROM chat_sessions
                ORDER BY created_at DESC
                """
            )

            sessions = cursor.fetchall()

        return [
            {
                "id": session[0],
                "title": session[1],
                "created_at": session[2]
            }
            for session in sessions
        ]

    finally:
        connection.close()


def get_chat_messages(
    session_id: int
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, role, content, created_at
                FROM chat_messages
                WHERE session_id = %s
                ORDER BY id ASC
                """,
                (session_id,)
            )

            messages = cursor.fetchall()

        return [
            {
                "id": message[0],
                "role": message[1],
                "content": message[2],
                "created_at": message[3]
            }
            for message in messages
        ]

    finally:
        connection.close()


def add_chat_message(
    session_id: int,
    role: str,
    content: str
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO chat_messages (
                    session_id,
                    role,
                    content
                )
                VALUES (%s, %s, %s)
                RETURNING id, session_id, role, content, created_at
                """,
                (
                    session_id,
                    role,
                    content
                )
            )

            message = cursor.fetchone()

        connection.commit()

        return {
            "id": message[0],
            "session_id": message[1],
            "role": message[2],
            "content": message[3],
            "created_at": message[4]
        }

    finally:
        connection.close()

def update_chat_title(
    session_id: int,
    title: str
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE chat_sessions
                SET title = %s
                WHERE id = %s
                """,
                (
                    title,
                    session_id
                )
            )

        connection.commit()

    finally:
        connection.close()

def update_chat_title(
    session_id: int,
    title: str
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE chat_sessions
                SET title = %s
                WHERE id = %s
                """,
                (
                    title,
                    session_id
                )
            )

        connection.commit()

    finally:
        connection.close()


def delete_chat_session(session_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM chat_sessions
                WHERE id = %s
                """,
                (session_id,)
            )

        connection.commit()

    finally:
        connection.close()