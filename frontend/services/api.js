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


export async function uploadDocument(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/documents/upload`,
    {
      method: "POST",
      body: formData
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Upload failed (${response.status})`
    );
  }

  return data;
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


export async function askQuestion(
  question,
  documentIds = null,
  conversation = [],
  onToken = null,
  onSources = null
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
        conversation
      })
    }
  );

  if (!response.ok) {
    let errorMessage = `Request failed (${response.status})`;

    try {
      const data = await response.json();

      errorMessage =
        data.detail ||
        errorMessage;
    } catch {
      // Response was not JSON.
    }

    throw new Error(errorMessage);
  }

  if (!response.body) {
    throw new Error(
      "Streaming response body is not available"
    );
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder();

  let buffer = "";

  let answer = "";

  let sources = [];

  while (true) {

    const { value, done } = await reader.read();

    if (done) {
      break;
    }

    buffer += decoder.decode(
      value,
      {
        stream: true
      }
    );

    const lines = buffer.split("\n");

    buffer = lines.pop();

    for (const line of lines) {

      if (!line.trim()) {
        continue;
      }

      const event = JSON.parse(line);

      if (event.type === "token") {

        answer += event.content;

        if (onToken) {
          onToken(event.content);
        }

      } else if (event.type === "sources") {

        sources = event.sources;

        if (onSources) {
          onSources(event.sources);
        }

      } else if (event.type === "complete") {

        answer = event.content;

        if (onToken) {
          onToken(event.content);
        }

      } else if (event.type === "error") {

        throw new Error(
          event.content ||
          "Streaming request failed"
        );
      }
    }
  }

  buffer += decoder.decode();

  if (buffer.trim()) {

    const event = JSON.parse(buffer);

    if (event.type === "token") {

      answer += event.content;

      if (onToken) {
        onToken(event.content);
      }

    } else if (event.type === "sources") {

      sources = event.sources;

      if (onSources) {
        onSources(event.sources);
      }

    } else if (event.type === "complete") {

      answer = event.content;

      if (onToken) {
        onToken(event.content);
      }

    } else if (event.type === "error") {

      throw new Error(
        event.content ||
        "Streaming request failed"
      );
    }
  }

  return {
    question,
    document_ids: documentIds,
    answer,
    sources
  };
}