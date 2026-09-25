import { useState } from "react";

import SourceDialog from "./SourceDialog";


function SourceCards({
  sources
}) {
  const [selectedSource, setSelectedSource] =
    useState(null);


  function openSource(source) {
    setSelectedSource(source);
  }


  function closeSource() {
    setSelectedSource(null);
  }


  function openPdf(source) {
    if (
      source?.document_id == null ||
      source?.page == null
    ) {
      return;
    }

    const pdfUrl =
      `http://127.0.0.1:8000/documents/${source.document_id}/pdf#page=${source.page}`;

    window.open(
      pdfUrl,
      "_blank",
      "noopener,noreferrer"
    );
  }


  return (
    <>
      <div className="source-cards-container">
        <div className="source-cards-header">
          <div>
            <h4>
              Sources used for this answer
            </h4>

            <p>
              Select a source to view the exact
              passage retrieved from your document.
            </p>
          </div>
        </div>

        <div className="source-cards-list">
          {sources.map((source, index) => (
            <button
              key={
                `${source.document_id}-${source.page}-${source.chunk}-${index}`
              }
              type="button"
              className="source-overview-card"
              onClick={() =>
                openSource(source)
              }
            >
              <div className="source-card-number">
                {index + 1}
              </div>

              <div className="source-overview-content">
                <div className="source-overview-title">
                  <span className="source-file-icon">
                    📄
                  </span>

                  <strong>
                    {source.source ||
                      "Document source"}
                  </strong>
                </div>

                <div className="source-overview-meta">
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

                <span className="source-card-action">
                  View retrieved passage →
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {selectedSource && (
        <SourceDialog
          source={selectedSource}
          sourceNumber={
            sources.indexOf(selectedSource) + 1
          }
          onClose={closeSource}
          onOpenPdf={openPdf}
        />
      )}
    </>
  );
}


export default SourceCards;