import { useState } from "react";

import { uploadDocument } from "../services/api";


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


    try {

      const data =
        await uploadDocument(
          selectedFile
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

      setError(
        error.message ||
        "Something went wrong while uploading the document."
      );

    } finally {

      setUploading(false);

    }
  }


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

                Processing...
              </>

            ) : (

              <>
                Upload PDF

                <span>
                  ↑
                </span>
              </>

            )}

          </button>

        </div>


        {uploadMessage && (

          <div className="success-message" role="status" aria-live="polite">

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