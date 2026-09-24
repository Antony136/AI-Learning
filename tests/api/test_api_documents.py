from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_documents():
    response = client.get("/documents")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_upload_invalid_file_type():
    files = {
        "file": (
            "test.txt",
            BytesIO(b"This is not a PDF"),
            "text/plain"
        )
    }

    response = client.post(
        "/documents/upload",
        files=files
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported"


def test_upload_missing_filename():
    files = {
        "file": (
            "",
            BytesIO(b"test"),
            "application/pdf"
        )
    }

    response = client.post(
        "/documents/upload",
        files=files
    )

    assert response.status_code in [400, 422]


def test_ask_empty_question():
    response = client.post(
        "/documents/ask",
        json={
            "question": ""
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Question cannot be empty"


def test_ask_whitespace_question():
    response = client.post(
        "/documents/ask",
        json={
            "question": "   "
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Question cannot be empty"


def test_ask_with_empty_document_ids():
    response = client.post(
        "/documents/ask",
        json={
            "question": "What is RAG?",
            "document_ids": []
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "document_ids cannot be empty"


def test_ask_with_nonexistent_document():
    response = client.post(
        "/documents/ask",
        json={
            "question": "What is RAG?",
            "document_ids": [999999]
        }
    )

    assert response.status_code == 404
    assert "Document 999999 not found" in response.json()["detail"]


def test_delete_nonexistent_document():
    response = client.delete("/documents/999999")

    assert response.status_code == 404
    assert "Document 999999 not found" in response.json()["detail"]