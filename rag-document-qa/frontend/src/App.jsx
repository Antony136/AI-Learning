import { useEffect, useState } from "react";
import "./App.css";


const API_URL = "http://127.0.0.1:8000";


function App() {

  const [documents, setDocuments] = useState([]);

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [sources, setSources] = useState([]);

  const [loading, setLoading] = useState(false);

  const [loadingDocuments, setLoadingDocuments] = useState(true);

  const [error, setError] = useState("");


  /*
   * Load documents when the application starts.
   */

  useEffect(() => {

    loadDocuments();

  }, []);


  /*
   * GET /documents
   */

  async function loadDocuments() {

    setLoadingDocuments(true);

    setError("");

    try {

      const response = await fetch(
        `${API_URL}/documents`
      );


      if (!response.ok) {

        throw new Error(
          `Failed to load documents (${response.status})`
        );

      }


      const data = await response.json();

      setDocuments(data);

    } catch (error) {

      console.error(error);

      setError(
        "Could not connect to the backend. " +
        "Make sure FastAPI is running on port 8000."
      );

    } finally {

      setLoadingDocuments(false);

    }

  }


  /*
   * Select / deselect a document.
   */

  function toggleDocument(documentId) {

    setSelectedDocuments((current) => {

      if (current.includes(documentId)) {

        return current.filter(
          (id) => id !== documentId
        );

      }


      return [
        ...current,
        documentId
      ];

    });

  }


  /*
   * Clear selected documents.
   */

  function clearSelection() {

    setSelectedDocuments([]);

  }


  /*
   * Ask the RAG system.
   */

  async function askQuestion() {

    if (!question.trim()) {
      return;
    }


    setLoading(true);

    setError("");

    setAnswer("");

    setSources([]);


    try {

      const response = await fetch(
        `${API_URL}/documents/ask`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            question: question.trim(),

            document_ids:
              selectedDocuments.length > 0
                ? selectedDocuments
                : null
          })
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          `Request failed (${response.status})`
        );

      }


      setAnswer(data.answer);

      setSources(data.sources || []);

    } catch (error) {

      console.error(error);

      setError(
        error.message ||
        "Something went wrong while asking the question."
      );

    } finally {

      setLoading(false);

    }

  }


  /*
   * Clear answer.
   */

  function clearAnswer() {

    setAnswer("");

    setSources([]);

    setError("");

  }


  /*
   * Allow Enter to submit while
   * Shift + Enter creates a new line.
   */

  function handleQuestionKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askQuestion();

    }

  }


  return (
    <div className="app">


      {/* =========================
          HEADER
      ========================== */}

      <header className="header">

        <div className="header-content">

          <div className="logo-area">

            <div className="logo-icon">
              R
            </div>

            <div>

              <h1>
                RAG Document Q&A
              </h1>

              <p>
                Ask questions about your documents
                using Retrieval-Augmented Generation.
              </p>

            </div>

          </div>

        </div>

      </header>


      {/* =========================
          MAIN
      ========================== */}

      <main className="container">


        {/* =========================
            DOCUMENTS
        ========================== */}

        <section className="card">

          <div className="section-header">

            <div>

              <h2>
                Documents
              </h2>

              <p className="section-description">
                Select the documents you want the
                AI to search.
              </p>

            </div>


            <div className="selection-info">

              <span>
                {selectedDocuments.length} selected
              </span>


              {selectedDocuments.length > 0 && (

                <button
                  className="clear-button"
                  onClick={clearSelection}
                >
                  Clear
                </button>

              )}

            </div>

          </div>


          <div className="documents-list">


            {loadingDocuments ? (

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
                  Upload a PDF to start asking
                  questions.
                </p>

              </div>

            ) : (

              documents.map((document) => (

                <label
                  key={document.id}
                  className={
                    `document-card ${
                      selectedDocuments.includes(document.id)
                        ? "selected"
                        : ""
                    }`
                  }
                >

                  <input
                    type="checkbox"
                    checked={selectedDocuments.includes(
                      document.id
                    )}
                    onChange={() =>
                      toggleDocument(document.id)
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

              ))

            )}

          </div>

        </section>


        {/* =========================
            QUESTION
        ========================== */}

        <section className="card">

          <div className="section-header">

            <div>

              <h2>
                Ask a question
              </h2>

              <p className="section-description">
                Ask something about the selected
                documents.
              </p>

            </div>

          </div>


          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleQuestionKeyDown}
            placeholder="Example: What is RAG and how does it work?"
            rows={5}
            disabled={loading}
          />


          <div className="question-footer">

            <span className="selection-hint">

              {selectedDocuments.length === 0

                ? "Searching all documents"

                : `Searching ${selectedDocuments.length} document${
                    selectedDocuments.length === 1
                      ? ""
                      : "s"
                  }`

              }

            </span>


            <button
              className="ask-button"
              onClick={askQuestion}
              disabled={
                loading ||
                !question.trim()
              }
            >

              {loading ? (

                <>
                  <span className="spinner"></span>
                  Thinking...
                </>

              ) : (

                <>
                  Ask Question
                  <span>→</span>
                </>

              )}

            </button>

          </div>

        </section>


        {/* =========================
            ERROR
        ========================== */}

        {error && (

          <div className="error-message">

            <div className="error-icon">
              !
            </div>

            <div>

              <strong>
                Something went wrong
              </strong>

              <p>
                {error}
              </p>

            </div>

          </div>

        )}


        {/* =========================
            ANSWER
        ========================== */}

        {answer && (

          <section className="card answer-card">

            <div className="answer-header">

              <div>

                <h2>
                  Answer
                </h2>

                <p className="section-description">
                  Generated using the retrieved
                  document context.
                </p>

              </div>


              <button
                className="clear-button"
                onClick={clearAnswer}
              >
                Clear
              </button>

            </div>


            <div className="answer-content">

              <p>
                {answer}
              </p>

            </div>


            {/* =========================
                SOURCES
            ========================== */}

            {sources.length > 0 && (

              <div className="sources">

                <div className="sources-header">

                  <h3>
                    Sources
                  </h3>

                  <span>
                    {sources.length} source
                    {sources.length === 1
                      ? ""
                      : "s"}
                  </span>

                </div>


                <div className="sources-list">

                  {sources.map(
                    (source, index) => (

                      <div
                        key={index}
                        className="source-card"
                      >

                        <div className="source-number">
                          {index + 1}
                        </div>


                        <div className="source-info">

                          <strong>
                            {source.source}
                          </strong>


                          <div className="source-meta">

                            <span>
                              Document{" "}
                              {source.document_id}
                            </span>

                            <span>
                              Page {source.page}
                            </span>

                            <span>
                              Chunk {source.chunk}
                            </span>

                          </div>

                        </div>

                      </div>

                    )
                  )}

                </div>

              </div>

            )}

          </section>

        )}

      </main>


      {/* =========================
          FOOTER
      ========================== */}

      <footer className="footer">

        <p>
          Local RAG system • PostgreSQL • pgvector
          • Ollama • FastAPI • React
        </p>

      </footer>

    </div>
  );
}


export default App;