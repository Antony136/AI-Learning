function ChatList({
  chats,
  currentSessionId,
  onSelectChat,
  onNewChat
}) {
  return (
    <aside
      className="chat-sidebar"
      aria-label="Chat sessions"
    >
      <div className="chat-sidebar-header">

        <h2>
          Chats
        </h2>

        <button
          type="button"
          className="new-chat-button"
          onClick={onNewChat}
        >
          + New Chat
        </button>

      </div>


      <div className="chat-sidebar-items">

        {chats.length === 0 ? (

          <p className="chat-list-empty">
            No chats yet.
          </p>

        ) : (

          chats.map((chat) => (

            <button
              key={chat.id}
              type="button"
              className={`chat-list-item ${
                chat.id === currentSessionId
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                onSelectChat(chat.id)
              }
            >
              <span className="chat-list-title">
                {chat.title}
              </span>
            </button>

          ))

        )}

      </div>

    </aside>
  );
}


export default ChatList;