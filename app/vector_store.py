from pathlib import Path
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


COLLECTION_NAME = "documents"
VECTOR_SIZE = 384
MIN_RELEVANCE_SCORE = 0.35

BASE_DIR = Path(__file__).resolve().parent.parent
QDRANT_PATH = BASE_DIR / "data" / "qdrant"
QDRANT_PATH.mkdir(parents=True, exist_ok=True)

client = QdrantClient(path=str(QDRANT_PATH))


def ensure_collection() -> None:
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    metadata: list[dict[str, object]] | None = None,
) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")

    if metadata is not None and len(metadata) != len(chunks):
        raise ValueError("metadata and chunks must have the same length")

    ensure_collection()

    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        payload: dict[str, object] = {"text": chunk}

        if metadata is not None:
            payload.update(metadata[index])

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload=payload,
            )
        )

    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )


def search_chunks(
    query_embedding: list[float],
    limit: int = 3,
) -> list[dict[str, object]]:
    if not query_embedding:
        raise ValueError("query_embedding must not be empty")

    if limit <= 0:
        raise ValueError("limit must be greater than 0")

    ensure_collection()

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        score_threshold=MIN_RELEVANCE_SCORE,
        with_payload=True,
    )

    results = []

    for point in response.points:
        payload = point.payload or {}

        results.append(
            {
                "text": payload.get("text", ""),
                "filename": payload.get("filename"),
                "page_number": payload.get("page_number"),
                "paragraph_number": payload.get("paragraph_number"),
                "score": point.score,
            }
        )

    return results