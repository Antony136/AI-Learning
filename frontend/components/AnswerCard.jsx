function AnswerCard({
  answer,
  conversation,
  pendingQuestion,
  loading,
  sources,
  onClear
}) {
  const hasConversation =
    conversation.length > 0 ||
    pendingQuestion ||
    loading ||
    answer;

  if (!hasConversation) {
    return (
      <section className="card chat-empty-state">
        <div className="chat-empty-icon">AI</div>
        <h2>Ask your documents anything</h2>
        <p>Select documents above or search your full knowledge base with a question.</p>
      </section>
    );
  }

  return (
    <section className="card answer-card chat-card">
      <div className="answer-header">
        <div>
          <h2>Conversation</h2>
          <p className="section-description">
            Questions and answers from this session.
          </p>
        </div>

        <button className="clear-button" onClick={onClear}>
          Clear conversation
        </button>
      </div>

      <div className="chat-messages" aria-live="polite">
        {conversation.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`chat-message ${message.role}`}
          >
            <span className="message-label">
              {message.role === "user" ? "You" : "AI"}
            </span>
            <div className="message-content">
              <p>{message.content}</p>
            </div>
          </div>
        ))}

        {pendingQuestion && (
          <div className="chat-message user pending-message">
            <span className="message-label">You</span>
            <div className="message-content">
              <p>{pendingQuestion}</p>
            </div>
          </div>
        )}

        {loading && (
          <div className="chat-message assistant thinking-message">
            <span className="message-label">AI</span>
            <div className="message-content thinking-content">
              <span className="spinner dark"></span>
              <span>Thinking...</span>
            </div>
          </div>
        )}
      </div>

      {sources.length > 0 && (
        <div className="sources">
          <div className="sources-header">
            <h3>Sources</h3>
            <span>
              {sources.length} source{sources.length === 1 ? "" : "s"}
            </span>
          </div>

          <div className="sources-list">
            {sources.map((source, index) => (
              <div
                key={`${source.document_id}-${source.page}-${source.chunk}-${index}`}
                className="source-card"
              >
                <div className="source-number">
                  {index + 1}
                </div>

                <div className="source-info">
                  <strong>{source.source}</strong>

                  <div className="source-meta">
                    <span>Document {source.document_id}</span>
                    <span>Page {source.page}</span>
                    <span>Chunk {source.chunk}</span>
                  </div>

                  {source.snippet && (
                    <p className="source-snippet">
                      {source.snippet}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

export default AnswerCard;