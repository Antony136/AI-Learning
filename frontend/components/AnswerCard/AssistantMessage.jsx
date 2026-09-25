import { useRef, useState } from "react";

import ReactMarkdown from "react-markdown";

import CopyButton from "./CopyButton";
import SourceCards from "./SourceCards";


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
  sources
}) {
  const contentRef = useRef(null);

  const [showSources, setShowSources] =
    useState(false);

  const hasSources =
    sources &&
    Array.isArray(sources) &&
    sources.length > 0;

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
          {hasSources && (
            <button
              type="button"
              className={`message-sources-button ${
                showSources
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                setShowSources(
                  (previous) =>
                    !previous
                )
              }
              aria-expanded={showSources}
              title="View sources used for this answer"
            >
              <span>📚</span>

              <span>
                {showSources
                  ? "Hide Sources"
                  : `${sources.length} Sources Used`}
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

        {hasSources && showSources && (
          <SourceCards
            sources={sources}
          />
        )}
      </div>
    </div>
  );
}


export default AssistantMessage;