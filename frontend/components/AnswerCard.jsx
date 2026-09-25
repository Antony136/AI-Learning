import { useEffect, useRef, useState } from "react";

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
  const messagesEndRef = useRef(null);
  const chatMessagesContainerRef = useRef(null);

  const hasConversation =
    conversation.length > 0 ||
    pendingQuestion ||
    loading ||
    answer;

  /*
   * Scroll smoothly when a new question is submitted or conversation changes
   */
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [conversation.length, pendingQuestion, loading]);

  const isEmpty =
    conversation.length === 0 &&
    !pendingQuestion &&
    !loading &&
    !answer;

  // Find the index of the last assistant message in conversation
  const lastAssistantIndex = conversation
    .map((m, i) => (m.role === "assistant" ? i : -1))
    .filter((i) => i !== -1)
    .pop();

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
              document.getElementById("question-box-card")?.scrollIntoView({ behavior: "smooth" });
            }}
            title="Go to Ask Question"
          >
            <span>↓</span> Ask Question
          </button>

          {conversation.length > 0 && (
            <button
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
        ref={chatMessagesContainerRef}
      >

        {isEmpty ? (
          <div className="conversation-empty-placeholder">
            <div className="chat-empty-icon">AI</div>
            <h3>Ask your documents anything</h3>
            <p>
              Type your question below to start a conversation with your document context.
            </p>
          </div>
        ) : (
          conversation.map((message, index) => (
            message.role === "assistant" ? (
              <AssistantMessage
                key={`${message.role}-${index}`}
                content={message.content}
                sources={message.sources}
                showInlineSourcesToggle={true}
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
          ))
        )}


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
            sources={sources}
            showInlineSourcesToggle={true}
          />
        )}

        <div ref={messagesEndRef} />

      </div>

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
  content,
  sources,
  showInlineSourcesToggle
}) {
  const contentRef = useRef(null);
  const [showInlineSources, setShowInlineSources] = useState(false);

  const hasSources = sources && Array.isArray(sources) && sources.length > 0;

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

          {hasSources && showInlineSourcesToggle && (
            <button
              type="button"
              className={`message-sources-button ${
                showInlineSources ? "active" : ""
              }`}
              onClick={() => setShowInlineSources((prev) => !prev)}
              title="Toggle Sources for this message"
            >
              <span>📚</span>
              <span>
                {showInlineSources
                  ? "Hide Sources"
                  : `Sources (${sources.length})`}
              </span>
            </button>
          )}

          <CopyButton
            getText={() =>
              contentRef.current?.innerText ||
              content
            }
          />

        </div>

        {hasSources && showInlineSourcesToggle && showInlineSources && (
          <div className="message-inline-sources">
            <h4>Referenced Sources</h4>

            <div className="sources-list">
              {sources.map((source, index) => (
                <div
                  key={`${source.document_id}-${source.page}-${source.chunk}-${index}`}
                  className="source-card compact"
                >
                  <div className="source-number">
                    {index + 1}
                  </div>

                  <div className="source-info">
                    {source.source && (
                      <strong>{source.source}</strong>
                    )}

                    <div className="source-meta">
                      {source.document_id != null && (
                        <span>Doc {source.document_id}</span>
                      )}

                      {source.page != null && (
                        <span>Page {source.page}</span>
                      )}

                      {source.chunk != null && (
                        <span>Chunk {source.chunk}</span>
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
          </div>
        )}

      </div>

    </div>
  );
}


export default AnswerCard;