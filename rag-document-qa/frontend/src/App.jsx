import { useEffect, useState } from "react";

import "./App.css";

import Header from "../components/Header";
import UploadDocument from "../components/UploadDocument";
import DocumentList from "../components/DocumentList";
import QuestionBox from "../components/QuestionBox";
import AnswerCard from "../components/AnswerCard";
import ErrorMessage from "../components/ErrorMessage";
import Footer from "../components/Footer";

import {
  getDocuments,
  askQuestion
} from "../services/api";


function App() {

  const [documents, setDocuments] =
    useState([]);

  const [selectedDocuments, setSelectedDocuments] =
    useState([]);

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [sources, setSources] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [loadingDocuments, setLoadingDocuments] =
    useState(true);

  const [error, setError] =
    useState("");


  /*
   * Load documents from backend.
   */
  async function loadDocuments() {

    setLoadingDocuments(true);

    setError("");

    try {

      const data =
        await getDocuments();

      setDocuments(data);

      /*
       * Keep only selected documents
       * that still exist.
       */
      setSelectedDocuments(
        (currentSelection) =>
          currentSelection.filter(
            (id) =>
              data.some(
                (document) =>
                  document.id === id
              )
          )
      );

    } catch (error) {

      console.error(error);

      setError(
        error.message ||
        "Could not load documents."
      );

    } finally {

      setLoadingDocuments(false);

    }
  }


  /*
   * Load documents when the application starts.
   */
  useEffect(() => {

    loadDocuments();

  }, []);


  /*
   * Select or deselect a document.
   */
  function toggleDocument(documentId) {

    setSelectedDocuments(
      (current) => {

        if (
          current.includes(documentId)
        ) {

          return current.filter(
            (id) =>
              id !== documentId
          );

        }

        return [
          ...current,
          documentId
        ];

      }
    );
  }


  /*
   * Clear all selected documents.
   */
  function clearSelection() {

    setSelectedDocuments([]);

  }


  /*
   * Remove a document from the
   * selected documents.
   */
  function removeFromSelection(
    documentId
  ) {

    setSelectedDocuments(
      (current) =>
        current.filter(
          (id) =>
            id !== documentId
        )
    );

  }


  /*
   * Ask a question.
   */
  async function handleAskQuestion() {

    if (!question.trim()) {
      return;
    }

    setLoading(true);

    setError("");

    setAnswer("");

    setSources([]);


    try {

      const data =
        await askQuestion(
          question.trim(),
          selectedDocuments.length > 0
            ? selectedDocuments
            : null
        );


      setAnswer(
        data.answer
      );

      setSources(
        data.sources || []
      );

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
   * Clear the current answer.
   */
  function clearAnswer() {

    setAnswer("");

    setSources([]);

    setError("");

  }


  return (

    <div className="app">

      <Header />


      <main className="container">

        <UploadDocument
          onUploadSuccess={
            loadDocuments
          }
          setError={setError}
        />


        <DocumentList
          documents={documents}
          selectedDocuments={
            selectedDocuments
          }
          onToggleDocument={
            toggleDocument
          }
          onClearSelection={
            clearSelection
          }
          onDocumentsChange={
            loadDocuments
          }
          onRemoveFromSelection={
            removeFromSelection
          }
          setError={setError}
          loading={
            loadingDocuments
          }
        />


        <QuestionBox
          question={question}
          setQuestion={setQuestion}
          onAskQuestion={
            handleAskQuestion
          }
          loading={loading}
          selectedDocuments={
            selectedDocuments
          }
        />


        <ErrorMessage
          error={error}
        />


        <AnswerCard
          answer={answer}
          sources={sources}
          onClear={clearAnswer}
        />

      </main>


      <Footer />

    </div>

  );
}


export default App;