import { useEffect, useRef, useState } from "react";


function ChatList({
  chats,
  currentSessionId,
  onSelectChat,
  onNewChat,
  onRenameChat,
  onDeleteChat
}) {
  const [openMenuId, setOpenMenuId] = useState(null);

  const [renameChatId, setRenameChatId] = useState(null);
  const [renameTitle, setRenameTitle] = useState("");

  const [deleteChatId, setDeleteChatId] = useState(null);

  const menuRef = useRef(null);


  /*
   * Close the action menu when clicking
   * anywhere outside of it.
   */
  useEffect(() => {
    function handleOutsideClick(event) {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target)
      ) {
        setOpenMenuId(null);
      }
    }

    document.addEventListener(
      "mousedown",
      handleOutsideClick
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleOutsideClick
      );
    };
  }, []);


  function openRenameDialog(chat) {
    setOpenMenuId(null);
    setRenameChatId(chat.id);
    setRenameTitle(chat.title);
  }


  function closeRenameDialog() {
    setRenameChatId(null);
    setRenameTitle("");
  }


  async function handleRename() {
    const title = renameTitle.trim();

    if (!title || !renameChatId) {
      return;
    }

    await onRenameChat(
      renameChatId,
      title
    );

    closeRenameDialog();
  }


  function openDeleteDialog(chatId) {
    setOpenMenuId(null);
    setDeleteChatId(chatId);
  }


  function closeDeleteDialog() {
    setDeleteChatId(null);
  }


  async function handleDelete() {
    if (!deleteChatId) {
      return;
    }

    await onDeleteChat(deleteChatId);

    closeDeleteDialog();
  }


  return (
    <>
      <aside
        className="chat-sidebar"
        aria-label="Chat sessions"
      >

        <div className="chat-sidebar-brand">
          <div className="chat-sidebar-logo">
            AI
          </div>

          <div>
            <h2>
              RAG Assistant
            </h2>

            <p>
              Document Q&A
            </p>
          </div>
        </div>


        <button
          type="button"
          className="new-chat-button"
          onClick={onNewChat}
        >
          <span className="new-chat-icon">
            +
          </span>

          <span>
            New chat
          </span>
        </button>


        <div className="chat-sidebar-section">

          <div className="chat-sidebar-section-title">
            Your chats
          </div>


          <div className="chat-sidebar-items">

            {chats.length === 0 ? (

              <div className="chat-sidebar-empty">
                <p>
                  No chats yet.
                </p>

                <span>
                  Start a new conversation.
                </span>
              </div>

            ) : (

              chats.map((chat) => (

                <div
                  key={chat.id}
                  className={`chat-item-row ${
                    chat.id === currentSessionId
                      ? "active"
                      : ""
                  }`}
                >

                  <button
                    type="button"
                    className="chat-list-item"
                    onClick={() =>
                      onSelectChat(chat.id)
                    }
                    title={chat.title}
                  >

                    <span className="chat-item-icon">
                      ◇
                    </span>

                    <span className="chat-list-title">
                      {chat.title}
                    </span>

                  </button>


                  <div
                    className="chat-item-actions"
                    ref={
                      openMenuId === chat.id
                        ? menuRef
                        : null
                    }
                  >

                    <button
                      type="button"
                      className="chat-action-button"
                      aria-label={`Actions for ${chat.title}`}
                      aria-expanded={
                        openMenuId === chat.id
                      }
                      onClick={(event) => {
                        event.stopPropagation();

                        setOpenMenuId(
                          openMenuId === chat.id
                            ? null
                            : chat.id
                        );
                      }}
                    >
                      ⋮
                    </button>


                    {openMenuId === chat.id && (

                      <div
                        className="chat-action-menu"
                        role="menu"
                      >

                        <button
                          type="button"
                          role="menuitem"
                          onClick={() =>
                            openRenameDialog(chat)
                          }
                        >
                          <span>✎</span>
                          Rename
                        </button>


                        <button
                          type="button"
                          role="menuitem"
                          className="danger"
                          onClick={() =>
                            openDeleteDialog(chat.id)
                          }
                        >
                          <span>🗑</span>
                          Delete
                        </button>

                      </div>

                    )}

                  </div>

                </div>

              ))

            )}

          </div>

        </div>


        <div className="chat-sidebar-footer">

          <div className="sidebar-footer-line" />

          <div className="sidebar-footer-info">
            <span className="sidebar-footer-dot" />

            <span>
              Local AI · Ollama
            </span>
          </div>

        </div>

      </aside>


      {renameChatId !== null && (

        <div
          className="chat-dialog-backdrop"
          role="presentation"
          onMouseDown={(event) => {
            if (
              event.target === event.currentTarget
            ) {
              closeRenameDialog();
            }
          }}
        >

          <div
            className="chat-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="rename-chat-title"
          >

            <h2 id="rename-chat-title">
              Rename chat
            </h2>

            <p>
              Give this conversation a new name.
            </p>


            <input
              type="text"
              value={renameTitle}
              onChange={(event) =>
                setRenameTitle(event.target.value)
              }
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleRename();
                }

                if (event.key === "Escape") {
                  closeRenameDialog();
                }
              }}
              maxLength={100}
              autoFocus
            />


            <div className="chat-dialog-actions">

              <button
                type="button"
                className="dialog-secondary-button"
                onClick={closeRenameDialog}
              >
                Cancel
              </button>

              <button
                type="button"
                className="dialog-primary-button"
                onClick={handleRename}
                disabled={!renameTitle.trim()}
              >
                Save
              </button>

            </div>

          </div>

        </div>

      )}


      {deleteChatId !== null && (

        <div
          className="chat-dialog-backdrop"
          role="presentation"
          onMouseDown={(event) => {
            if (
              event.target === event.currentTarget
            ) {
              closeDeleteDialog();
            }
          }}
        >

          <div
            className="chat-dialog delete-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="delete-chat-title"
          >

            <div className="delete-dialog-icon">
              !
            </div>

            <h2 id="delete-chat-title">
              Delete this chat?
            </h2>

            <p>
              This conversation and all of its
              messages will be permanently deleted.
            </p>


            <div className="chat-dialog-actions">

              <button
                type="button"
                className="dialog-secondary-button"
                onClick={closeDeleteDialog}
              >
                Cancel
              </button>

              <button
                type="button"
                className="dialog-danger-button"
                onClick={handleDelete}
              >
                Delete
              </button>

            </div>

          </div>

        </div>

      )}

    </>
  );
}


export default ChatList;