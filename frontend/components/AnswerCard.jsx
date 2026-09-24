import { useRef, useState } from "react";

import ReactMarkdown from "react-markdown";


function AnswerCard({
  answer,
  conversation,
  pendingQuestion,
  loading,
  sources,
  onClear
}) {
  const [showSources, setShowSources] = useState(false);

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
        <p>
          Select documents above or search your full knowledge base with a question.
        </p>
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

        <button
          className="clear-button"
          onClick={onClear}
        >
          Clear conversation
        </button>
      </div>


      <div className="chat-messages" aria-live="polite">

        {conversation.map((message, index) => (
          message.role === "assistant" ? (
            <AssistantMessage
              key={`${message.role}-${index}`}
              content={message.content}
            />
          ) : (
            <div
              key={`${message.role}-${index}`}
              className="chat-message user"
            >
              <span className="message-label">You</span>

              <div className="message-content">
                <p>{message.content}</p>
              </div>
            </div>
          )
        ))}


        {pendingQuestion && (
          <div className="chat-message user pending-message">
            <span className="message-label">You</span>

            <div className="message-content">
              <p>{pendingQuestion}</p>
            </div>
          </div>
        )}


        {loading && !answer && (
          <div className="chat-message assistant thinking-message">
            <span className="message-label">AI</span>

            <div className="message-content thinking-content">
              <span className="spinner dark"></span>
              <span>Thinking...</span>
            </div>
          </div>
        )}


        {loading && answer && (
          <AssistantMessage
            content={answer}
          />
        )}

      </div>


      {sources.length > 0 && (
        <div className="sources">

          <button
            type="button"
            className="sources-toggle"
            aria-expanded={showSources}
            aria-controls="answer-sources-list"
            onClick={() =>
              setShowSources((current) => !current)
            }
          >
            <span className="source-toggle-copy">
              <strong>Sources</strong>

              <span className="source-toggle-state">
                {showSources
                  ? "Hide sources"
                  : "Show sources"}
              </span>
            </span>

            <span className="source-count">
              {sources.length} source
              {sources.length === 1 ? "" : "s"}
            </span>

            <span
              className="source-toggle-icon"
              aria-hidden="true"
            />
          </button>


          {showSources && (
            <div
              id="answer-sources-list"
              className="sources-list"
            >

              {sources.map((source, index) => (
                <div
                  key={`${source.document_id}-${source.page}-${source.chunk}-${index}`}
                  className="source-card"
                >

                  <div className="source-number">
                    {index + 1}
                  </div>

                  <div className="source-info">

                    {source.source && (
                      <strong>
                        {source.source}
                      </strong>
                    )}

                    <div className="source-meta">

                      {source.document_id != null && (
                        <span>
                          Document {source.document_id}
                        </span>
                      )}

                      {source.page != null && (
                        <span>
                          Page {source.page}
                        </span>
                      )}

                      {source.chunk != null && (
                        <span>
                          Chunk {source.chunk}
                        </span>
                      )}

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
          )}

        </div>
      )}

    </section>
  );
}


function CopyButton({
  text,
  getText,
  className = ""
}) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      const value = getText
        ? getText()
        : text;

      await navigator.clipboard.writeText(value);

      setCopied(true);

      window.setTimeout(() => {
        setCopied(false);
      }, 1600);

    } catch (error) {
      console.error(
        "Could not copy text.",
        error
      );
    }
  }

  return (
    <button
      type="button"
      className={`copy-button ${className}`}
      onClick={handleCopy}
      aria-label={
        copied
          ? "Copied"
          : "Copy"
      }
    >
      {copied
        ? "Copied"
        : "Copy"}
    </button>
  );
}


function CodeBlock({
  children,
  language
}) {
  const code = String(children);

  return (
    <div className="markdown-code-block">

      <div className="code-block-header">
        <span>
          {language || "Code"}
        </span>

        <CopyButton text={code} />
      </div>

      <pre>
        <code>{code}</code>
      </pre>

    </div>
  );
}


function AssistantMessage({
  content
}) {
  const contentRef = useRef(null);

  return (
    <div className="chat-message assistant">

      <span className="message-label">
        AI
      </span>

      <div className="message-content">

        <div
          ref={contentRef}
          className="markdown-content"
        >

          <ReactMarkdown
            components={{
              code({
                inline,
                className,
                children,
                ...props
              }) {
                if (inline) {
                  return (
                    <code
                      className="markdown-inline-code"
                      {...props}
                    >
                      {children}
                    </code>
                  );
                }

                const language =
                  className?.replace(
                    "language-",
                    ""
                  );

                return (
                  <CodeBlock
                    language={language}
                  >
                    {children}
                  </CodeBlock>
                );
              },

              a({
                children,
                ...props
              }) {
                return (
                  <a
                    target="_blank"
                    rel="noreferrer"
                    {...props}
                  >
                    {children}
                  </a>
                );
              }
            }}
          >
            {content}
          </ReactMarkdown>

        </div>

        <div className="message-actions">
          <CopyButton
            getText={() =>
              contentRef.current?.innerText ||
              content
            }
          />
        </div>

      </div>

    </div>
  );
}


export default AnswerCard;