import { useRef } from "react";

import AssistantMessage from "./AssistantMessage";
import "./AnswerCard.css";

function AnswerCard({
  answer,
  conversation,
  pendingQuestion,
  loading,
  sources,
  onClear
}) {
  const messagesEndRef = useRef(null);

  const isEmpty =
    conversation.length === 0 &&
    !pendingQuestion &&
    !loading &&
    !answer;

  return (
    <section className="card answer-card chat-card">
      <div className="answer-header">
        <div>
          <h2>Conversation</h2>

          <p className="section-description">
            Questions and answers from this session.
          </p>
        </div>

        <div className="answer-header-actions">
          <button
            type="button"
            className="jump-to-ask-button"
            onClick={() => {
              document
                .getElementById("question-box-card")
                ?.scrollIntoView({
                  behavior: "smooth"
                });
            }}
            title="Go to Ask Question"
          >
            <span>↓</span> Ask Question
          </button>

          {conversation.length > 0 && (
            <button
              type="button"
              className="clear-button"
              onClick={onClear}
            >
              Clear conversation
            </button>
          )}
        </div>
      </div>

      <div
        className="chat-messages"
        aria-live="polite"
      >
        {isEmpty ? (
          <div className="conversation-empty-placeholder">
            <div className="chat-empty-icon">
              AI
            </div>

            <h3>
              Ask your documents anything
            </h3>

            <p>
              Type your question below to start
              a conversation with your document
              context.
            </p>
          </div>
        ) : (
          conversation.map((message, index) => (
            message.role === "assistant" ? (
              <AssistantMessage
                key={`${message.role}-${index}`}
                content={message.content}
                sources={message.sources}
              />
            ) : (
              <div
                key={`${message.role}-${index}`}
                className="chat-message user"
              >
                <span className="message-label">
                  You
                </span>

                <div className="message-content">
                  <p>{message.content}</p>
                </div>
              </div>
            )
          ))
        )}

        {pendingQuestion && (
          <div className="chat-message user pending-message">
            <span className="message-label">
              You
            </span>

            <div className="message-content">
              <p>{pendingQuestion}</p>
            </div>
          </div>
        )}

        {loading && !answer && (
          <div className="chat-message assistant thinking-message">
            <span className="message-label">
              AI
            </span>

            <div className="message-content thinking-content">
              <span className="spinner dark"></span>

              <span>
                Thinking...
              </span>
            </div>
          </div>
        )}

        {loading && answer && (
          <AssistantMessage
            content={answer}
            sources={sources}
          />
        )}

        <div ref={messagesEndRef} />
      </div>
    </section>
  );
}


export default AnswerCard;