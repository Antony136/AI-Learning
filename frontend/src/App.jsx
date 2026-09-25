import { useEffect, useState } from "react";

import "./App.css";

import Header from "../components/Header";
import UploadDocument from "../components/UploadDocument/UploadDocument";
import DocumentList from "../components/DocumentList/DocumentList";
import ChatList from "../components/ChatList/ChatList";
import QuestionBox from "../components/QuestionBox";
import AnswerCard from "../components/AnswerCard/AnswerCard";
import ErrorMessage from "../components/ErrorMessage";
import Footer from "../components/Footer";

import {
  getDocuments,
  getChats,
  createChat,
  getChat,
  renameChat,
  deleteChat,
  askQuestion
} from "../services/api";


function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocuments, setSelectedDocuments] = useState([]);

  const [chats, setChats] = useState([]);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const [conversation, setConversation] = useState([]);
  const [pendingQuestion, setPendingQuestion] = useState("");

  const [sessionId, setSessionId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [loadingChat, setLoadingChat] = useState(true);

  const [error, setError] = useState("");


  /*
   * Load documents from backend.
   */
  async function loadDocuments() {
    setLoadingDocuments(true);
    setError("");

    try {
      const data = await getDocuments();

      setDocuments(data);

      /*
       * Keep only selected documents
       * that still exist.
       */
      setSelectedDocuments((currentSelection) =>
        currentSelection.filter((id) =>
          data.some(
            (document) => document.id === id
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
   * Load all chat sessions.
   */
  async function loadChats() {
    try {
      const data = await getChats();

      setChats(data);

      return data;

    } catch (error) {
      console.error(error);

      setError(
        error.message ||
        "Could not load chats."
      );

      return [];
    }
  }


  /*
   * Load a specific chat session.
   */
  async function loadChatSession(
    targetSessionId
  ) {
    setLoadingChat(true);

    try {

      const data =
        await getChat(
          targetSessionId
        );


      setSessionId(
        data.session.id
      );


      localStorage.setItem(
        "rag_chat_session_id",
        String(data.session.id)
      );


      const rawMessages = data.messages.map((message) => ({
        role: message.role,
        content: message.content
      }));

      // Restore per-message sources from localStorage
      let storedSourcesMap = {};
      try {
        storedSourcesMap = JSON.parse(
          localStorage.getItem(`rag_chat_sources_${targetSessionId}`) || "{}"
        );
      } catch {
        storedSourcesMap = {};
      }

      const restoredConversation = rawMessages.map((msg, idx) => {
        if (msg.role === "assistant" && storedSourcesMap[idx]) {
          return {
            ...msg,
            sources: storedSourcesMap[idx]
          };
        }
        return msg;
      });

      setConversation(restoredConversation);

      // Restore sources for the latest prompt if available
      const lastAssistantWithSources = [...restoredConversation]
        .reverse()
        .find((msg) => msg.role === "assistant" && msg.sources && msg.sources.length > 0);

      setAnswer("");
      setSources(lastAssistantWithSources?.sources || []);
      setPendingQuestion("");
      setQuestion("");


    } catch (error) {

      console.error(error);

      setError(
        error.message ||
        "Could not load chat."
      );

    } finally {

      setLoadingChat(false);
    }
  }


  /*
   * Load or create the persistent chat session.
   */
  async function initializeChat() {
    setLoadingChat(true);

    try {

      const availableChats =
        await getChats();


      setChats(
        availableChats
      );


      const savedSessionId =
        localStorage.getItem(
          "rag_chat_session_id"
        );


      /*
       * Try to restore the previously
       * selected chat.
       */
      if (savedSessionId) {

        const savedId =
          Number(savedSessionId);


        const savedChat =
          availableChats.find(
            (chat) =>
              chat.id === savedId
          );


        if (savedChat) {

          await loadChatSession(
            savedId
          );

          return;
        }


        /*
         * Saved session no longer exists.
         */
        localStorage.removeItem(
          "rag_chat_session_id"
        );
      }


      /*
       * No valid session exists.
       *
       * Create a new chat.
       */
      const newSession =
        await createChat();


      setSessionId(
        newSession.id
      );


      localStorage.setItem(
        "rag_chat_session_id",
        String(newSession.id)
      );


      setConversation([]);


      /*
       * Add the newly created chat
       * to the chat list.
       */
      setChats(
        (currentChats) => [
          newSession,
          ...currentChats
        ]
      );


    } catch (error) {

      console.error(error);

      setError(
        error.message ||
        "Could not initialize chat."
      );

    } finally {

      setLoadingChat(false);
    }
  }


  /*
   * Create a completely new chat.
   */
  async function handleNewChat() {

    if (loading) {
      return;
    }


    try {

      setLoadingChat(true);
      setError("");


      const newSession =
        await createChat();


      setSessionId(
        newSession.id
      );


      localStorage.setItem(
        "rag_chat_session_id",
        String(newSession.id)
      );


      setConversation([]);
      setAnswer("");
      setSources([]);
      setPendingQuestion("");
      setQuestion("");


      setChats(
        (currentChats) => [
          newSession,
          ...currentChats
        ]
      );


    } catch (error) {

      console.error(error);

      setError(
        error.message ||
        "Could not create a new chat."
      );

    } finally {

      setLoadingChat(false);
    }
  }


  /*
   * Switch to another existing chat.
   */
  async function handleSelectChat(
    selectedSessionId
  ) {

    if (
      loading ||
      selectedSessionId === sessionId
    ) {
      return;
    }


    await loadChatSession(
      selectedSessionId
    );
  }

  async function handleRenameChat(
  chatId,
  title
) {
  try {
    setError("");

    const updatedChat =
      await renameChat(
        chatId,
        title
      );

    setChats((currentChats) =>
      currentChats.map((chat) =>
        chat.id === chatId
          ? {
              ...chat,
              title: updatedChat.title
            }
          : chat
      )
    );

  } catch (error) {
    console.error(error);

    setError(
      error.message ||
      "Could not rename chat."
    );

    throw error;
  }
}


async function handleDeleteChat(
  chatId
) {
  try {
    setError("");

    await deleteChat(chatId);

    const updatedChats =
      chats.filter(
        (chat) => chat.id !== chatId
      );

    setChats(updatedChats);


    if (chatId === sessionId) {

      if (updatedChats.length > 0) {

        await loadChatSession(
          updatedChats[0].id
        );

      } else {

        await handleNewChat();

      }

    }

  } catch (error) {
    console.error(error);

    setError(
      error.message ||
      "Could not delete chat."
    );

    throw error;
  }
}
  /*
   * Load documents and chat when
   * the application starts.
   */
  useEffect(() => {
    loadDocuments();
    initializeChat();
  }, []);


  /*
   * Select or deselect a document.
   */
  function toggleDocument(documentId) {
    setSelectedDocuments((current) => {
      if (current.includes(documentId)) {
        return current.filter(
          (id) => id !== documentId
        );
      }

      return [...current, documentId];
    });
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
  function removeFromSelection(documentId) {
    setSelectedDocuments((current) =>
      current.filter(
        (id) => id !== documentId
      )
    );
  }


  /*
   * Ask a question.
   */
  async function handleAskQuestion() {

    if (
      !question.trim() ||
      loading ||
      loadingChat ||
      !sessionId
    ) {
      return;
    }


    const currentQuestion =
      question.trim();


    setPendingQuestion(
      currentQuestion
    );

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);
    setQuestion("");


    try {

      const data =
        await askQuestion(
          currentQuestion,

          selectedDocuments.length > 0
            ? selectedDocuments
            : null,

          sessionId,


          /*
           * Called whenever a new LLM token arrives.
           */
          (token) => {
            setAnswer((currentAnswer) =>
              currentAnswer + token
            );
          },


          /*
           * Called when retrieval sources arrive.
           */
          (newSources) => {
            setSources(newSources);
          },


          /*
           * Called when the backend
           * returns the session ID.
           */
          (returnedSessionId) => {

            setSessionId(
              returnedSessionId
            );

            localStorage.setItem(
              "rag_chat_session_id",
              String(returnedSessionId)
            );
          }
        );


      /*
       * Make sure the final answer is exactly
       * what the streaming API returned.
       */
      setAnswer(
        data.answer
      );

      setSources(
        data.sources || []
      );


      /*
       * Add the completed question and answer
       * to the local conversation, with persistent sources.
       */
      const finalSources = data.sources || [];

      setConversation((currentConversation) => {
        const updated = [
          ...currentConversation,
          {
            role: "user",
            content: currentQuestion
          },
          {
            role: "assistant",
            content: data.answer,
            sources: finalSources
          }
        ];

        // Save sources map to localStorage for this session
        try {
          const sourcesMap = {};
          updated.forEach((msg, idx) => {
            if (msg.role === "assistant" && msg.sources && msg.sources.length > 0) {
              sourcesMap[idx] = msg.sources;
            }
          });
          localStorage.setItem(`rag_chat_sources_${sessionId}`, JSON.stringify(sourcesMap));
        } catch (e) {
          console.error("Could not cache sources to localStorage:", e);
        }

        return updated;
      });


      /*
       * Refresh chat list because the
       * selected chat may eventually
       * receive an updated title.
       */
      await loadChats();


      setPendingQuestion("");


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
   * Clear the currently displayed
   * conversation.
   *
   * The database session is intentionally
   * kept for now.
   */
  function clearAnswer() {

    setAnswer("");
    setSources([]);
    setConversation([]);
    setPendingQuestion("");
    setError("");
  }


  return (
    <div className="app">

      <Header />

      <main className="app-layout">

        <ChatList
          chats={chats}
          currentSessionId={sessionId}
          onSelectChat={handleSelectChat}
          onNewChat={handleNewChat}
          onRenameChat={handleRenameChat}
          onDeleteChat={handleDeleteChat}
        />

        <div className="main-content">

          <UploadDocument
            onUploadSuccess={loadDocuments}
            setError={setError}
          />

          <DocumentList
            documents={documents}
            selectedDocuments={selectedDocuments}
            onToggleDocument={toggleDocument}
            onClearSelection={clearSelection}
            onDocumentsChange={loadDocuments}
            onRemoveFromSelection={
              removeFromSelection
            }
            setError={setError}
            loading={loadingDocuments}
          />

          <AnswerCard
            answer={answer}
            conversation={conversation}
            pendingQuestion={pendingQuestion}
            loading={loading}
            sources={sources}
            onClear={clearAnswer}
          />

          <ErrorMessage
            error={error}
          />

          <QuestionBox
            question={question}
            setQuestion={setQuestion}
            onAskQuestion={handleAskQuestion}
            loading={
              loading ||
              loadingChat
            }
            selectedDocuments={selectedDocuments}
          />

        </div>

      </main>

      <Footer />

    </div>
  );
}


export default App;