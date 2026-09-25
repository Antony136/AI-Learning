import { useState } from "react";

import { uploadDocument } from "../../services/api";
import "./UploadDocument.css";


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


function getStageDescription(stage) {
  const descriptions = {
    extracting:
      "Reading the text and page structure from your PDF.",

    chunking:
      "Breaking the document into searchable sections.",

    embedding:
      "Converting document chunks into semantic vectors.",

    storing:
      "Saving the chunks and embeddings for retrieval.",

    ready:
      "Your document is ready for questions.",

    failed:
      "Something went wrong while processing the document."
  };

  return (
    descriptions[stage] ||
    "Processing your document."
  );
}


function getProgressPercentage(
  stage,
  current,
  total
) {
  if (stage === "ready") {
    return 100;
  }

  if (!total || total <= 0) {
    return 0;
  }

  const stageProgress =
    Math.min(
      current / total,
      1
    );

  const stageRanges = {
    extracting: {
      start: 0,
      end: 15
    },

    chunking: {
      start: 15,
      end: 30
    },

    embedding: {
      start: 30,
      end: 75
    },

    storing: {
      start: 75,
      end: 100
    }
  };

  const range =
    stageRanges[stage];

  if (!range) {
    return 0;
  }

  return (
    range.start +
    (
      (range.end - range.start) *
      stageProgress
    )
  );
}


const stages = [
  "extracting",
  "chunking",
  "embedding",
  "storing"
];


function getStageState(
  stage,
  currentStage
) {
  const currentIndex =
    stages.indexOf(currentStage);

  const stageIndex =
    stages.indexOf(stage);

  if (currentStage === "ready") {
    return "completed";
  }

  if (currentStage === "failed") {
    return stage === currentStage
      ? "failed"
      : "pending";
  }

  if (stageIndex < currentIndex) {
    return "completed";
  }

  if (stage === currentStage) {
    return "active";
  }

  return "pending";
}


function UploadDocument({
  onUploadSuccess,
  setError
}) {

  const [selectedFile, setSelectedFile] =
    useState(null);

  const [uploading, setUploading] =
    useState(false);

  const [uploadMessage, setUploadMessage] =
    useState("");

  const [uploadStage, setUploadStage] =
    useState("");

  const [uploadCurrent, setUploadCurrent] =
    useState(0);

  const [uploadTotal, setUploadTotal] =
    useState(0);


  function handleFileChange(event) {

    const file =
      event.target.files?.[0];

    setUploadMessage("");

    setError("");


    if (!file) {

      setSelectedFile(null);

      return;
    }


    if (
      file.type !== "application/pdf" &&
      !file.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {

      setSelectedFile(null);

      setError(
        "Only PDF files are supported."
      );

      event.target.value = "";

      return;
    }


    setSelectedFile(file);
  }


  async function handleUpload() {

    if (!selectedFile) {

      setError(
        "Please select a PDF first."
      );

      return;
    }


    setUploading(true);

    setError("");

    setUploadMessage("");

    setUploadStage("extracting");

    setUploadCurrent(0);

    setUploadTotal(0);


    try {

      const data = await uploadDocument(
        selectedFile,
        (
          stage,
          current,
          total
        ) => {

          setUploadStage(stage);

          setUploadCurrent(
            current || 0
          );

          setUploadTotal(
            total || 0
          );

        }
      );


      setUploadStage("ready");

      setUploadCurrent(
        data.chunks || 0
      );

      setUploadTotal(
        data.chunks || 0
      );


      setUploadMessage(
        `${data.filename} is ready. ` +
        `${data.pages} pages, ` +
        `${data.chunks} chunks, ` +
        `${formatFileSize(data.file_size)}.`
      );


      setSelectedFile(null);


      const fileInput =
        document.getElementById(
          "pdf-upload"
        );


      if (fileInput) {
        fileInput.value = "";
      }


      if (onUploadSuccess) {
        await onUploadSuccess();
      }

    } catch (error) {

      console.error(error);

      setUploadStage("failed");

      setError(
        error.message ||
        "Something went wrong while uploading the document."
      );

    } finally {

      setUploading(false);

    }
  }


  const progressPercentage =
    getProgressPercentage(
      uploadStage,
      uploadCurrent,
      uploadTotal
    );


  return (

    <section className="card">

      <div className="section-header">

        <div>

          <h2>
            Upload a document
          </h2>

          <p className="section-description">
            Upload a PDF to add it to your
            knowledge base.
          </p>

        </div>

      </div>


      <div className="upload-area">

        <input
          id="pdf-upload"
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          disabled={uploading}
        />


        <div className="upload-controls">

          <label
            htmlFor="pdf-upload"
            className="file-button"
          >
            Choose PDF
          </label>


          <span className="selected-file">

            {selectedFile ? (
              <span title={selectedFile.name}>
                {selectedFile.name}
              </span>
            ) : (
              "No file selected"
            )}

          </span>


          <button
            className="upload-button"
            onClick={handleUpload}
            disabled={
              uploading ||
              !selectedFile
            }
          >

            {uploading ? (
              <>
                <span className="spinner"></span>
                Processing
              </>
            ) : (
              <>
                Upload PDF
                <span>↑</span>
              </>
            )}

          </button>

        </div>


        {uploading && uploadStage && (

          <div
            className="upload-progress-panel"
            role="status"
            aria-live="polite"
          >

            <div className="upload-progress-top">

              <div>

                <strong>
                  Processing document
                </strong>

                <p>
                  {getStageDescription(
                    uploadStage
                  )}
                </p>

              </div>


              <span className="upload-progress-percent">
                {Math.round(
                  progressPercentage
                )}%
              </span>

            </div>


            <div className="upload-progress-track">

              <div
                className="upload-progress-bar"
                style={{
                  width: `${progressPercentage}%`
                }}
              />

            </div>


            <div className="upload-stage-list">

              {stages.map(
                (stage) => {

                  const state =
                    getStageState(
                      stage,
                      uploadStage
                    );

                  return (

                    <div
                      key={stage}
                      className={`upload-stage ${state}`}
                    >

                      <span className="upload-stage-indicator">

                        {state === "completed" && "✓"}

                        {state === "active" && (
                          <span className="spinner tiny"></span>
                        )}

                      </span>


                      <span className="upload-stage-name">
                        {getStageLabel(stage)}
                      </span>


                      {state === "active" &&
                        uploadTotal > 0 && (

                          <span className="upload-stage-count">

                            {uploadCurrent} /{" "}
                            {uploadTotal}

                            {stage === "chunking"
                              ? " pages"
                              : " chunks"}

                          </span>

                        )}

                    </div>

                  );
                }
              )}

            </div>

          </div>

        )}


        {uploadMessage && (

          <div
            className="success-message"
            role="status"
            aria-live="polite"
          >

            <div className="success-icon">
              ✓
            </div>


            <div>

              <strong>
                Upload successful
              </strong>

              <p>
                {uploadMessage}
              </p>

            </div>

          </div>

        )}

      </div>

    </section>

  );
}


export default UploadDocument;