import json
import queue
import threading
from pathlib import Path

from app.core.database import get_connection
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from app.storage.documents import get_documents, get_document
from app.storage.chunks import get_document_status
from app.storage.chats import (
    create_chat_session,
    get_chat_session,
    get_chat_sessions,
    get_chat_messages,
    add_chat_message,
    update_chat_title,
    delete_chat_session
)

from app.ingestion.pipeline import ingest_document
from app.rag import answer_question_stream
from app.generation.sources import build_sources


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

DOCUMENTS_DIR = Path("documents")


class ChatMessage(BaseModel):
    role: str
    content: str

class RenameChatRequest(BaseModel):
    title: str

class QuestionRequest(BaseModel):
    question: str
    document_ids: list[int] | None = None
    session_id: int | None = None


@router.get("")
def list_documents():
    return get_documents()

@router.get("/{document_id}/pdf")
def get_document_pdf(document_id: int):
    document = get_document(document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    file_path = document.get("file_path")

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="PDF file path not found."
        )

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found on server."
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{document["filename"]}"'
        }
    )

@router.get("/{document_id}/sources/{chunk_id}")
def get_source_chunk(document_id: int, chunk_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    dc.id,
                    dc.document_id,
                    dc.source,
                    dc.page,
                    dc.chunk_index,
                    dc.content,
                    d.filename,
                    d.file_path
                FROM document_chunks dc
                JOIN documents d
                    ON dc.document_id = d.id
                WHERE dc.document_id = %s
                  AND dc.id = %s
                """,
                (document_id, chunk_id)
            )

            row = cursor.fetchone()

            if not row:
                raise HTTPException(
                    status_code=404,
                    detail="Source chunk not found."
                )

            return {
                "chunk_id": row[0],
                "document_id": row[1],
                "source": row[2],
                "page": row[3],
                "chunk": row[4],
                "content": row[5],
                "filename": row[6],
                "file_path": row[7]
            }

    finally:
        connection.close()


@router.get("/{document_id}/status")
def document_status(document_id: int):

    document = get_document_status(
        document_id
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return document


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    DOCUMENTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = DOCUMENTS_DIR / file.filename

    try:

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(
                contents
            )

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


    def stream_upload():

        progress_queue = queue.Queue()

        def on_progress(stage, current=0, total=0):
            progress_queue.put(
                {
                    "type": "progress",
                    "stage": stage,
                    "current": current,
                    "total": total
                }
            )


        result_container = {
            "result": None,
            "error": None
        }


        def run_ingestion():

            try:

                result_container["result"] = (
                    ingest_document(
                        str(file_path),
                        on_progress=on_progress
                    )
                )

            except Exception as error:

                result_container["error"] = error

            finally:

                progress_queue.put(
                    None
                )


        thread = threading.Thread(
            target=run_ingestion,
            daemon=True
        )

        thread.start()


        while True:

            event = progress_queue.get()

            if event is None:
                break

            yield (
                json.dumps(event)
                + "\n"
            )


        if result_container["error"]:

            yield (
                json.dumps(
                    {
                        "type": "error",
                        "content": str(
                            result_container["error"]
                        )
                    }
                )
                + "\n"
            )

        else:

            yield (
                json.dumps(
                    {
                        "type": "complete",
                        "document":
                            result_container["result"]
                    }
                )
                + "\n"
            )


    return StreamingResponse(
        stream_upload(),
        media_type="application/x-ndjson"
    )


@router.post("/ask")
def ask_documents(
    request: QuestionRequest
):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if request.document_ids is not None:

        if not request.document_ids:
            raise HTTPException(
                status_code=400,
                detail="document_ids cannot be empty"
            )

        for document_id in request.document_ids:

            document = get_document(
                document_id
            )

            if document is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Document {document_id} not found"
                )

    if request.session_id is not None:

        session = get_chat_session(
            request.session_id
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail=f"Chat session {request.session_id} not found"
            )

    else:

        session = create_chat_session()

    session_id = session["id"]

    stored_messages = get_chat_messages(
        session_id
    )

    conversation = [
        ChatMessage(
            role=message["role"],
            content=message["content"]
        )
        for message in stored_messages
    ]

    def generate():

        assistant_answer = ""

        try:

            for event in answer_question_stream(
                question=request.question,
                document_ids=request.document_ids,
                conversation=conversation
            ):

                if event["type"] == "token":

                    assistant_answer += event["content"]

                    yield json.dumps(event) + "\n"

                elif event["type"] == "complete":

                    assistant_answer = event["content"]

                    yield json.dumps(event) + "\n"

                elif event["type"] == "sources":

                    event = {
                        "type": "sources",
                        "sources": build_sources(
                            event["sources"]
                        )
                    }

                    yield json.dumps(event) + "\n"

                if event["type"] == "done":

                    stored_messages = get_chat_messages(
                        session_id
                    )

                    is_first_message = (
                        len(stored_messages) == 0
                    )


                    add_chat_message(
                        session_id=session_id,
                        role="user",
                        content=request.question.strip()
                    )


                    if assistant_answer:

                        add_chat_message(
                            session_id=session_id,
                            role="assistant",
                            content=assistant_answer
                        )


                    if is_first_message:

                        title = request.question.strip()

                        if len(title) > 50:
                            title = title[:50].rstrip() + "..."

                        update_chat_title(
                            session_id=session_id,
                            title=title
                        )


                    yield json.dumps({
                        "type": "session",
                        "session_id": session_id
                    }) + "\n"


                    yield json.dumps(event) + "\n"

        except Exception as error:

            yield json.dumps({
                "type": "error",
                "content": str(error)
            }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"
    )

@router.get("/chats")
def list_chats():
    return get_chat_sessions()

@router.post("/chats")
def create_chat():
    return create_chat_session()


@router.get("/chats/{session_id}")
def get_chat(session_id: int):

    session = get_chat_session(
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Chat session {session_id} not found"
        )

    messages = get_chat_messages(
        session_id
    )

    return {
        "session": session,
        "messages": messages
    }

@router.patch("/chats/{session_id}")
def rename_chat(
    session_id: int,
    request: RenameChatRequest
):
    session = get_chat_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Chat session {session_id} not found"
        )

    title = request.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Chat title cannot be empty"
        )

    if len(title) > 100:
        raise HTTPException(
            status_code=400,
            detail="Chat title cannot exceed 100 characters"
        )

    update_chat_title(
        session_id=session_id,
        title=title
    )

    return {
        "id": session_id,
        "title": title
    }


@router.delete("/chats/{session_id}")
def delete_chat(session_id: int):
    session = get_chat_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Chat session {session_id} not found"
        )

    delete_chat_session(session_id)

    return {
        "message": "Chat deleted successfully",
        "session_id": session_id
    }

@router.delete("/{document_id}")
def delete_document(document_id: int):

    document = get_document(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document {document_id} not found"
        )

    from app.core.database import get_connection

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM documents
                WHERE id = %s
                """,
                (document_id,)
            )

        connection.commit()

    except Exception:

        connection.rollback()
        raise

    finally:

        connection.close()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id,
        "filename": document["filename"]
    }