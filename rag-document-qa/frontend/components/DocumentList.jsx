import { deleteDocument } from "../services/api";


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


      /*
       * Remove document from
       * selected documents.
       */
      onRemoveFromSelection(
        documentId
      );


      /*
       * Refresh document list.
       */
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

    <section className="card">

      <div className="section-header">

        <div>

          <h2>
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
              onClick={
                onClearSelection
              }
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
            (document) => (

              <div
                key={document.id}
                className={`document-card ${
                  selectedDocuments.includes(
                    document.id
                  )
                    ? "selected"
                    : ""
                }`}
              >

                <label className="document-main">

                  <input
                    type="checkbox"
                    checked={
                      selectedDocuments.includes(
                        document.id
                      )
                    }
                    onChange={() =>
                      onToggleDocument(
                        document.id
                      )
                    }
                  />


                  <div className="document-icon">
                    PDF
                  </div>


                  <div className="document-info">

                    <strong>
                      {document.filename}
                    </strong>

                    <span>
                      {document.chunk_count} chunks
                    </span>

                  </div>


                  <div className="document-check">

                    {selectedDocuments.includes(
                      document.id
                    ) && "✓"}

                  </div>

                </label>


                <button
                  className="delete-button"
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

            )
          )

        )}

      </div>

    </section>

  );
}


export default DocumentList;