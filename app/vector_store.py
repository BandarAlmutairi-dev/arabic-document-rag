from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

COLLECTION_NAME = "documents"
VECTOR_SIZE = 384

client = QdrantClient(":memory:")


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
) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")

    ensure_collection()

    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={"text": chunk},
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )