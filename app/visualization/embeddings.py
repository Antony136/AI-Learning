import numpy as np
from sklearn.decomposition import PCA

from app.core.database import get_connection
from app.ingestion.embeddings import generate_embedding
from app.retrieval.search import retrieve

def _load_embeddings(
    document_ids: list[int] | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if document_ids is not None:

                if not document_ids:
                    return []

                placeholders = ", ".join(
                    ["%s"] * len(document_ids)
                )

                query = f"""
                    SELECT
                        id,
                        document_id,
                        source,
                        page,
                        chunk_index,
                        content,
                        embedding::text
                    FROM document_chunks
                    WHERE document_id IN ({placeholders})
                      AND embedding IS NOT NULL
                    ORDER BY id
                """

                cursor.execute(
                    query,
                    document_ids
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        id,
                        document_id,
                        source,
                        page,
                        chunk_index,
                        content,
                        embedding::text
                    FROM document_chunks
                    WHERE embedding IS NOT NULL
                    ORDER BY id
                    """
                )

            rows = cursor.fetchall()

        embeddings = []

        for row in rows:

            embedding_text = row[6]

            values = (
                embedding_text
                .strip("[]")
                .split(",")
            )

            embedding = [
                float(value)
                for value in values
            ]

            embeddings.append(embedding)

        return rows, embeddings

    finally:
        connection.close()


def get_embedding_points(
    document_ids: list[int] | None = None
):
    result = _load_embeddings(
        document_ids=document_ids
    )

    if not result:
        return []

    rows, embeddings = result

    if not rows:
        return []

    embedding_dimensions = {
        len(embedding)
        for embedding in embeddings
    }

    if len(embedding_dimensions) != 1:
        raise ValueError(
            "Stored embeddings have inconsistent dimensions: "
            f"{embedding_dimensions}"
        )

    # PCA needs at least two points.
    if len(embeddings) < 2:
        return [
            {
                "id": row[0],
                "document_id": row[1],
                "source": row[2],
                "page": row[3],
                "chunk_index": row[4],
                "content": row[5],
                "x": 0.0,
                "y": 0.0
            }
            for row in rows
        ]

    embedding_matrix = np.asarray(
        embeddings,
        dtype=np.float32
    )

    pca = PCA(
        n_components=2
    )

    coordinates = pca.fit_transform(
        embedding_matrix
    )

    points = []

    for row, coordinate in zip(
        rows,
        coordinates
    ):
        points.append(
            {
                "id": row[0],
                "document_id": row[1],
                "source": row[2],
                "page": row[3],
                "chunk_index": row[4],
                "content": row[5],
                "x": float(coordinate[0]),
                "y": float(coordinate[1])
            }
        )

    return points

def get_query_embedding_point(
    question: str,
    document_ids: list[int] | None = None
):
    result = _load_embeddings(
        document_ids=document_ids
    )

    if not result:
        return None

    rows, embeddings = result

    if len(embeddings) < 2:
        return None

    embedding_dimensions = {
        len(embedding)
        for embedding in embeddings
    }

    if len(embedding_dimensions) != 1:
        raise ValueError(
            "Stored embeddings have inconsistent dimensions: "
            f"{embedding_dimensions}"
        )

    document_matrix = np.asarray(
        embeddings,
        dtype=np.float32
    )

    # Generate embedding for the user's question.
    query_embedding = generate_embedding(
        question
    )

    query_vector = np.asarray(
        query_embedding,
        dtype=np.float32
    )

    if query_vector.shape[0] != document_matrix.shape[1]:
        raise ValueError(
            "Query embedding dimension does not match "
            "stored document embeddings."
        )

    # Fit PCA using the document embeddings.
    pca = PCA(
        n_components=2
    )

    pca.fit(
        document_matrix
    )

    # Project the query into the SAME PCA space.
    query_coordinates = pca.transform(
        query_vector.reshape(1, -1)
    )[0]

    return {
        "x": float(query_coordinates[0]),
        "y": float(query_coordinates[1]),
        "question": question
    }

def get_query_visualization(
    question: str,
    document_ids: list[int] | None = None,
    retrieval_top_k: int = 5
):
    result = _load_embeddings(
        document_ids=document_ids
    )

    if not result:
        return None

    rows, embeddings = result

    if len(embeddings) < 2:
        return None

    embedding_dimensions = {
        len(embedding)
        for embedding in embeddings
    }

    if len(embedding_dimensions) != 1:
        raise ValueError(
            "Stored embeddings have inconsistent dimensions: "
            f"{embedding_dimensions}"
        )

    document_matrix = np.asarray(
        embeddings,
        dtype=np.float32
    )

    # --------------------------------------------------
    # 1. Fit PCA using document embeddings
    # --------------------------------------------------

    pca = PCA(
        n_components=2
    )

    document_coordinates = pca.fit_transform(
        document_matrix
    )

    # --------------------------------------------------
    # 2. Generate query embedding
    # --------------------------------------------------

    query_embedding = generate_embedding(
        question
    )

    query_vector = np.asarray(
        query_embedding,
        dtype=np.float32
    )

    if query_vector.shape[0] != document_matrix.shape[1]:
        raise ValueError(
            "Query embedding dimension does not match "
            "stored document embeddings."
        )

    # --------------------------------------------------
    # 3. Project query into same PCA space
    # --------------------------------------------------

    query_coordinates = pca.transform(
        query_vector.reshape(1, -1)
    )[0]

    # --------------------------------------------------
    # 4. Run ACTUAL vector retrieval
    # --------------------------------------------------

    retrieved_results = retrieve(
        question=question,
        top_k=retrieval_top_k,
        max_distance=0.50,
        document_ids=document_ids
    )

    retrieved_ids = {
        result["id"]
        for result in retrieved_results
    }

    # --------------------------------------------------
    # 5. Build document points
    # --------------------------------------------------

    points = []

    for row, coordinate in zip(
        rows,
        document_coordinates
    ):

        chunk_id = row[0]

        retrieved_result = next(
            (
                result
                for result in retrieved_results
                if result["id"] == chunk_id
            ),
            None
        )

        points.append(
            {
                "id": chunk_id,
                "document_id": row[1],
                "source": row[2],
                "page": row[3],
                "chunk_index": row[4],
                "content": row[5],
                "x": float(coordinate[0]),
                "y": float(coordinate[1]),
                "retrieved": chunk_id in retrieved_ids,
                "distance": (
                    retrieved_result["distance"]
                    if retrieved_result
                    else None
                )
            }
        )

    return {
        "query": {
            "question": question,
            "x": float(query_coordinates[0]),
            "y": float(query_coordinates[1])
        },
        "points": points,
        "retrieved_count": len(retrieved_results)
    }