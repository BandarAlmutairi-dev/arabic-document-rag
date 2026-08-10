import pytest
from qdrant_client import QdrantClient

import app.vector_store as vector_store


@pytest.fixture(autouse=True)
def isolated_vector_store(monkeypatch):
    test_client = QdrantClient(":memory:")
    monkeypatch.setattr(vector_store, "client", test_client)

    yield

    test_client.close()


def test_ensure_collection():
    vector_store.ensure_collection()

    assert vector_store.client.collection_exists(
        vector_store.COLLECTION_NAME
    )


def test_store_chunks():
    chunks = ["النص الأول", "النص الثاني"]
    embeddings = [
        [0.1] * 384,
        [0.2] * 384,
    ]

    vector_store.store_chunks(chunks, embeddings)

    count = vector_store.client.count(
        collection_name=vector_store.COLLECTION_NAME,
        exact=True,
    ).count

    assert count == 2


def test_mismatched_chunks_and_embeddings():
    with pytest.raises(ValueError):
        vector_store.store_chunks(
            ["نص واحد"],
            [[0.1] * 384, [0.2] * 384],
        )


def test_search_chunks():
    embedding = [1.0] + [0.0] * 383

    vector_store.store_chunks(
        ["مستند عن الذكاء الاصطناعي"],
        [embedding],
    )

    results = vector_store.search_chunks(
        query_embedding=embedding,
        limit=1,
    )

    assert len(results) == 1
    assert results[0]["text"] == "مستند عن الذكاء الاصطناعي"


def test_empty_query_embedding():
    with pytest.raises(ValueError):
        vector_store.search_chunks([])


def test_store_and_search_with_metadata():
    embedding = [0.0, 1.0] + [0.0] * 382

    vector_store.store_chunks(
        ["هذه معلومة من الصفحة الثانية"],
        [embedding],
        metadata=[
            {
                "filename": "sample.pdf",
                "page_number": 2,
            }
        ],
    )

    results = vector_store.search_chunks(
        query_embedding=embedding,
        limit=1,
    )

    assert results[0]["filename"] == "sample.pdf"
    assert results[0]["page_number"] == 2