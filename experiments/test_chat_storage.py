from app.storage.chats import (
    create_chat_session,
    get_chat_session,
    get_chat_messages,
    add_chat_message,
)


session = create_chat_session(
    "Test Chat"
)

print("Created session:")
print(session)


add_chat_message(
    session["id"],
    "user",
    "What is RAG?"
)


add_chat_message(
    session["id"],
    "assistant",
    "RAG combines retrieval with generation."
)


print("\nSession:")
print(
    get_chat_session(
        session["id"]
    )
)


print("\nMessages:")
print(
    get_chat_messages(
        session["id"]
    )
)