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
  conversation = []
) {
  const response = await fetch(`${API_URL}/documents/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      question,
      document_ids: documentIds,
      conversation
    })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || `Request failed (${response.status})`
    );
  }

  return data;
}