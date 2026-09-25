import { useEffect } from "react";


function SourceDialog({
  source,
  sourceNumber,
  onClose,
  onOpenPdf
}) {
  useEffect(() => {
    function handleEscape(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    document.addEventListener(
      "keydown",
      handleEscape
    );

    return () => {
      document.removeEventListener(
        "keydown",
        handleEscape
      );
    };
  }, [onClose]);


  return (
    <div
      className="source-dialog-overlay"
      onMouseDown={(event) => {
        if (
          event.target ===
          event.currentTarget
        ) {
          onClose();
        }
      }}
    >
      <div
        className="source-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="source-dialog-title"
      >
        <div className="source-dialog-header">
          <div>
            <span className="source-dialog-label">
              Source {sourceNumber}
            </span>

            <h3 id="source-dialog-title">
              {source.source ||
                "Document source"}
            </h3>

            <div className="source-dialog-meta">
              {source.page != null && (
                <span>
                  📍 Page {source.page}
                </span>
              )}

              {source.chunk != null && (
                <span>
                  Chunk {source.chunk}
                </span>
              )}
            </div>
          </div>

          <button
            type="button"
            className="source-dialog-close"
            onClick={onClose}
            aria-label="Close source"
          >
            ×
          </button>
        </div>

        <div className="source-dialog-body">
          <div className="source-dialog-explanation">
            <span>📖</span>

            <p>
              This is the exact passage retrieved
              from your document and provided to
              the AI as context for this answer.
            </p>
          </div>

          <div className="source-dialog-content">
            {source.snippet ? (
              <p>
                {source.snippet}
              </p>
            ) : (
              <p className="source-empty-text">
                No retrieved passage is available.
              </p>
            )}
          </div>
        </div>

        <div className="source-dialog-footer">
          <button
            type="button"
            className="source-dialog-secondary-button"
            onClick={onClose}
          >
            Close
          </button>

          {source.document_id != null &&
            source.page != null && (
              <button
                type="button"
                className="source-dialog-primary-button"
                onClick={() =>
                  onOpenPdf(source)
                }
              >
                ↗ Open PDF — Page{" "}
                {source.page}
              </button>
            )}
        </div>
      </div>
    </div>
  );
}


export default SourceDialog;