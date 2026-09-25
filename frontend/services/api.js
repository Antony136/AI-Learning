const API_URL = "http://127.0.0.1:8000";


export async function getDocuments() {
  const response = await fetch(
    `${API_URL}/documents`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load documents (${response.status})`
    );
  }

  return response.json();
}


export async function uploadDocument(
  file,
  onStage
) {
  const formData = new FormData();

  formData.append(
    "file",
    file
  );


  const response = await fetch(
    `${API_URL}/documents/upload`,
    {
      method: "POST",
      body: formData
    }
  );


  /*
   * Handle normal HTTP errors
   * before attempting to read the stream.
   */
  if (!response.ok) {

    let message =
      "Could not upload document.";

    try {

      const data =
        await response.json();

      message =
        data.detail ||
        message;

    } catch {
      // Keep default message.
    }

    throw new Error(
      message
    );
  }


  /*
   * The backend sends NDJSON progress
   * events through a streaming response.
   */
  if (!response.body) {

    throw new Error(
      "Upload streaming is not supported by this browser."
    );
  }


  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();


  let buffer = "";


  /*
   * Read the upload/processing stream.
   */
  while (true) {

    const {
      value,
      done
    } = await reader.read();


    if (done) {
      break;
    }


    buffer += decoder.decode(
      value,
      {
        stream: true
      }
    );


    const lines =
      buffer.split("\n");


    /*
     * Keep the incomplete final line
     * for the next network chunk.
     */
    buffer =
      lines.pop() || "";


    for (const line of lines) {

      if (!line.trim()) {
        continue;
      }


      const event =
        JSON.parse(line);


      /*
       * Example:
       * {"type":"stage","stage":"embedding"}
       */
      if (event.type === "progress") {

        if (onStage) {
          onStage(
            event.stage,
            event.current,
            event.total
          );
        }

      }


      /*
       * Example:
       * {
       *   "type": "complete",
       *   "document": {...}
       * }
       */
      else if (
        event.type === "complete"
      ) {

        return event.document;

      }


      /*
       * Example:
       * {
       *   "type": "error",
       *   "content": "..."
       * }
       */
      else if (
        event.type === "error"
      ) {

        throw new Error(
          event.content ||
          "Document processing failed."
        );

      }

    }

  }


  /*
   * Flush any remaining decoder data.
   */
  buffer +=
    decoder.decode();


  /*
   * Process a final event if one
   * remained in the buffer.
   */
  if (buffer.trim()) {

    const event =
      JSON.parse(buffer);


    if (
      event.type === "complete"
    ) {

      return event.document;

    }


    if (
      event.type === "error"
    ) {

      throw new Error(
        event.content ||
        "Document processing failed."
      );

    }

  }


  /*
   * The backend ended the stream without
   * telling us that processing completed.
   */
  throw new Error(
    "Upload ended without a completion event."
  );
}

export async function deleteDocument(documentId) {
  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      method: "DELETE"
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Delete failed (${response.status})`
    );
  }

  return data;
}

/*
 * Load all persistent chat sessions.
 */
export async function getChats() {
  const response = await fetch(
    `${API_URL}/documents/chats`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Could not load chats (${response.status})`
    );
  }

  return data;
}

/*
 * Create a new persistent chat session.
 */
export async function createChat() {
  const response = await fetch(
    `${API_URL}/documents/chats`,
    {
      method: "POST"
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Could not create chat (${response.status})`
    );
  }

  return data;
}


/*
 * Load an existing persistent chat session.
 */
export async function getChat(sessionId) {
  const response = await fetch(
    `${API_URL}/documents/chats/${sessionId}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Could not load chat (${response.status})`
    );
  }

  return data;
}

export async function renameChat(sessionId, title) {
  const response = await fetch(
    `${API_URL}/documents/chats/${sessionId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title
      })
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || `Could not rename chat (${response.status})`
    );
  }

  return data;
}


export async function deleteChat(sessionId) {
  const response = await fetch(
    `${API_URL}/documents/chats/${sessionId}`,
    {
      method: "DELETE"
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || `Could not delete chat (${response.status})`
    );
  }

  return data;
}

/*
 * Ask a question using a persistent chat session.
 */
export async function askQuestion(
  question,
  documentIds = null,
  sessionId = null,
  onToken = null,
  onSources = null,
  onSession = null
) {
  const response = await fetch(
    `${API_URL}/documents/ask`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        question,
        document_ids: documentIds,
        session_id: sessionId
      })
    }
  );


  /*
   * Handle normal HTTP errors
   * before attempting to read the stream.
   */
  if (!response.ok) {

    let errorMessage =
      `Request failed (${response.status})`;

    try {

      const data =
        await response.json();

      errorMessage =
        data.detail ||
        errorMessage;

    } catch {
      // Response was not JSON.
    }

    throw new Error(
      errorMessage
    );
  }


  if (!response.body) {
    throw new Error(
      "Streaming response body is not available"
    );
  }


  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();


  let buffer = "";

  let answer = "";

  let sources = [];

  let returnedSessionId =
    sessionId;


  /*
   * Process streaming NDJSON events.
   */
  while (true) {

    const {
      value,
      done
    } = await reader.read();


    if (done) {
      break;
    }


    buffer += decoder.decode(
      value,
      {
        stream: true
      }
    );


    const lines =
      buffer.split("\n");


    /*
     * Keep the incomplete final line
     * for the next chunk.
     */
    buffer =
      lines.pop();


    for (const line of lines) {

      if (!line.trim()) {
        continue;
      }


      const event =
        JSON.parse(line);


      if (event.type === "token") {

        answer +=
          event.content;


        if (onToken) {
          onToken(
            event.content
          );
        }

      }


      else if (
        event.type === "sources"
      ) {

        sources =
          event.sources;


        if (onSources) {
          onSources(
            event.sources
          );
        }

      }


      else if (
        event.type === "complete"
      ) {

        answer =
          event.content;


        if (onToken) {
          onToken(
            event.content
          );
        }

      }


      else if (
        event.type === "session"
      ) {

        returnedSessionId =
          event.session_id;


        if (onSession) {
          onSession(
            event.session_id
          );
        }

      }


      else if (
        event.type === "error"
      ) {

        throw new Error(
          event.content ||
          "Streaming request failed"
        );
      }
    }
  }


  /*
   * Process any final buffered event.
   */
  buffer +=
    decoder.decode();


  if (buffer.trim()) {

    const event =
      JSON.parse(buffer);


    if (event.type === "token") {

      answer +=
        event.content;


      if (onToken) {
        onToken(
          event.content
        );
      }

    }


    else if (
      event.type === "sources"
    ) {

      sources =
        event.sources;


      if (onSources) {
        onSources(
          event.sources
        );
      }

    }


    else if (
      event.type === "complete"
    ) {

      answer =
        event.content;


      if (onToken) {
        onToken(
          event.content
        );
      }

    }


    else if (
      event.type === "session"
    ) {

      returnedSessionId =
        event.session_id;


      if (onSession) {
        onSession(
          event.session_id
        );
      }

    }


    else if (
      event.type === "error"
    ) {

      throw new Error(
        event.content ||
        "Streaming request failed"
      );
    }
  }


  return {
    question,
    document_ids: documentIds,
    session_id: returnedSessionId,
    answer,
    sources
  };
}