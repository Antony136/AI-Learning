import { deleteDocument } from "../services/api";


function formatFileSize(bytes) {
  if (!bytes) {
    return "Size unavailable";
  }

  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}


function formatDate(dateValue) {
  if (!dateValue) {
    return "";
  }

  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleDateString(
    undefined,
    {
      day: "numeric",
      month: "short",
      year: "numeric"
    }
  );
}


function getStageLabel(stage) {
  const labels = {
    extracting: "Extracting text",
    chunking: "Creating chunks",
    embedding: "Generating embeddings",
    storing: "Storing in PostgreSQL",
    ready: "Ready",
    failed: "Processing failed"
  };

  return labels[stage] || "Processing";
}


function DocumentStatus({ document }) {
  if (document.status === "ready") {
    return (
      <span className="document-status ready">
        <span className="document-status-icon">
          ✓
        </span>
        Ready
      </span>
    );
  }

  if (document.status === "failed") {
    return (
      <span className="document-status failed">
        <span className="document-status-icon">
          !
        </span>
        Failed
      </span>
    );
  }

  return (
    <span className="document-status processing">
      <span className="spinner small"></span>
      {getStageLabel(document.stage)}
    </span>
  );
}


function DocumentList({
  documents,
  selectedDocuments,
  onToggleDocument,
  onClearSelection,
  onDocumentsChange,
  onRemoveFromSelection,
  setError,
  loading
}) {

  async function handleDelete(
    documentId,
    filename
  ) {

    const confirmed = window.confirm(
      `Are you sure you want to delete "${filename}"?\n\n` +
      "This will remove the document and all of its stored chunks."
    );

    if (!confirmed) {
      return;
    }

    setError("");

    try {

      await deleteDocument(
        documentId
      );

      onRemoveFromSelection(
        documentId
      );

      await onDocumentsChange();

    } catch (error) {

      console.error(error);

      setError(
        error.message ||
        "Something went wrong while deleting the document."
      );
    }
  }


  return (

    <section
      className="card"
      aria-labelledby="documents-heading"
    >

      <div className="section-header">

        <div>

          <h2 id="documents-heading">
            Documents
          </h2>

          <p className="section-description">
            Select the documents you want
            the AI to search.
          </p>

        </div>


        <div className="selection-info">

          <span>
            {selectedDocuments.length} selected
          </span>


          {selectedDocuments.length > 0 && (

            <button
              className="clear-button"
              onClick={onClearSelection}
            >
              Clear
            </button>

          )}

        </div>

      </div>


      <div className="documents-list">

        {loading ? (

          <div className="empty-state">

            <div className="spinner dark"></div>

            <p>
              Loading documents...
            </p>

          </div>

        ) : documents.length === 0 ? (

          <div className="empty-state">

            <div className="empty-icon">
              📄
            </div>

            <h3>
              No documents found
            </h3>

            <p>
              Upload a PDF to start
              asking questions.
            </p>

          </div>

        ) : (

          documents.map(
            (document) => {

              const isSelected =
                selectedDocuments.includes(
                  document.id
                );

              return (

                <div
                  key={document.id}
                  className={`document-card ${
                    isSelected
                      ? "selected"
                      : ""
                  } ${
                    document.status === "processing"
                      ? "processing"
                      : ""
                  } ${
                    document.status === "failed"
                      ? "failed"
                      : ""
                  }`}
                >

                  <label className="document-main">

                    <input
                      type="checkbox"
                      aria-label={`Select ${document.filename}`}
                      checked={isSelected}
                      onChange={() =>
                        onToggleDocument(
                          document.id
                        )
                      }
                      disabled={
                        document.status !== "ready"
                      }
                    />


                    <div className="document-icon">
                      PDF
                    </div>


                    <div className="document-info">

                      <div className="document-title-row">

                        <strong
                          title={document.filename}
                        >
                          {document.filename}
                        </strong>

                        <DocumentStatus
                          document={document}
                        />

                      </div>


                      {document.status === "ready" ? (

                        <div className="document-metadata">

                          <span>
                            {document.page_count ?? 0} pages
                          </span>

                          <span className="metadata-separator">
                            •
                          </span>

                          <span>
                            {document.chunk_count ?? 0} chunks
                          </span>

                          <span className="metadata-separator">
                            •
                          </span>

                          <span>
                            {formatFileSize(
                              document.file_size
                            )}
                          </span>

                        </div>

                      ) : (

                        <div className="document-processing-text">

                          {getStageLabel(
                            document.stage
                          )}

                        </div>

                      )}


                      {document.created_at && (

                        <span className="document-date">
                          Uploaded{" "}
                          {formatDate(
                            document.created_at
                          )}
                        </span>

                      )}

                    </div>


                    <div className="document-check">

                      {isSelected && "✓"}

                    </div>

                  </label>


                  <button
                    className="delete-button"
                    aria-label={`Delete ${document.filename}`}
                    onClick={() =>
                      handleDelete(
                        document.id,
                        document.filename
                      )
                    }
                    title="Delete document"
                  >
                    Delete
                  </button>

                </div>

              );
            }
          )

        )}

      </div>

    </section>

  );
}


export default DocumentList;