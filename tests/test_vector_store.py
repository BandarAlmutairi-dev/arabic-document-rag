import pytest

from app.vector_store import (
    COLLECTION_NAME,
    client,
    ensure_collection,
    store_chunks,
)


def test_ensure_collection():
    ensure_collection()

    assert client.collection_exists(COLLECTION_NAME)


def test_store_chunks():
    chunks = ["النص الأول", "النص الثاني"]
    embeddings = [
        [0.1] * 384,
        [0.2] * 384,
    ]

    store_chunks(chunks, embeddings)

    count = client.count(
        collection_name=COLLECTION_NAME,
        exact=True,
    ).count

    assert count >= 2


def test_mismatched_chunks_and_embeddings():
    with pytest.raises(ValueError):
        store_chunks(
            ["نص واحد"],
            [[0.1] * 384, [0.2] * 384],
        )