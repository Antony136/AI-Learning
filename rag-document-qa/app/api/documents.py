from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

from app.storage.documents import get_documents, get_document
from app.ingestion.pipeline import ingest_document
from app.rag import answer_question


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

DOCUMENTS_DIR = Path("documents")


class QuestionRequest(BaseModel):
    question: str
    document_ids: list[int] | None = None


@router.get("")
def list_documents():
    return get_documents()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

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

        with open(file_path, "wb") as output_file:
            output_file.write(contents)

        result = ingest_document(
            str(file_path)
        )

        return {
            "message": "Document uploaded and ingested successfully",
            **result
        }

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(error)
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

        documents = []

        for document_id in request.document_ids:

            document = get_document(
                document_id
            )

            if document is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Document {document_id} not found"
                )

            documents.append(document)

    try:

        answer, results = answer_question(
            question=request.question,
            document_ids=request.document_ids
        )

        sources = [
            {
                "document_id": result["document_id"],
                "source": result["source"],
                "page": result["page"],
                "chunk": result["chunk_index"]
            }
            for result in results
        ]

        return {
            "question": request.question,
            "document_ids": request.document_ids,
            "answer": answer,
            "sources": sources
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )