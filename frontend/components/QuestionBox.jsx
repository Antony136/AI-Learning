function QuestionBox({
  question,
  setQuestion,
  onAskQuestion,
  loading,
  selectedDocuments
}) {

  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      onAskQuestion();

    }
  }


  return (

    <section className="card">

      <div className="section-header">

        <div>

          <h2>
            Ask a question
          </h2>

          <p className="section-description">
            Ask something about the
            selected documents.
          </p>

        </div>

      </div>


      <textarea
        value={question}
        onChange={(event) =>
          setQuestion(
            event.target.value
          )
        }
        onKeyDown={handleKeyDown}
        placeholder="Example: What is RAG and how does it work?"
        rows={5}
        disabled={loading}
      />


      <div className="question-footer">

        <span className="selection-hint">

          {selectedDocuments.length === 0
            ? "Searching all documents"
            : `Searching ${
                selectedDocuments.length
              } document${
                selectedDocuments.length === 1
                  ? ""
                  : "s"
              }`}

        </span>


        <button
          className="ask-button"
          onClick={onAskQuestion}
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

  );
}


export default QuestionBox;