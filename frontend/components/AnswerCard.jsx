function AnswerCard({ answer, sources, onClear }) {
  if (!answer) return null;

  return (
    <section className="card answer-card">
      <div className="answer-header">
        <div>
          <h2>Answer</h2>
          <p className="section-description">
            Generated using the retrieved document context.
          </p>
        </div>

        <button className="clear-button" onClick={onClear}>
          Clear
        </button>
      </div>

      <div className="answer-content">
        <p>{answer}</p>
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