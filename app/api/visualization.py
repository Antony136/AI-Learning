from fastapi import APIRouter, Query

from app.visualization.embeddings import (
    get_embedding_points,
    get_query_visualization,
)


router = APIRouter(
    prefix="/visualization",
    tags=["Visualization"]
)


@router.get("/embeddings")
def get_embeddings(
    document_ids: list[int] | None = Query(
        default=None
    )
):
    points = get_embedding_points(
        document_ids=document_ids
    )

    return {
        "count": len(points),
        "points": points
    }


@router.get("/query")
def visualize_query(
    question: str,
    document_ids: list[int] | None = Query(
        default=None
    ),
    retrieval_top_k: int = 5
):
    result = get_query_visualization(
        question=question,
        document_ids=document_ids,
        retrieval_top_k=retrieval_top_k
    )

    if result is None:
        return {
            "query": None,
            "points": [],
            "retrieved_count": 0
        }

    return result