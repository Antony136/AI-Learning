from fastapi import FastAPI

from app.api.documents import router as documents_router


app = FastAPI(
    title="RAG Document Q&A",
    description="AI-powered document question answering system",
    version="1.0.0"
)


app.include_router(documents_router)


@app.get("/")
def root():
    return {
        "message": "RAG Document Q&A API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }