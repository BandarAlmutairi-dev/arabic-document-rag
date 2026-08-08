import pytest

from app.vector_store import (
    COLLECTION_NAME,
    client,
    ensure_collection,
    search_chunks,
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


def test_search_chunks():
    embedding = [1.0] + [0.0] * 383

    store_chunks(
        ["مستند عن الذكاء الاصطناعي"],
        [embedding],
    )

    results = search_chunks(
        query_embedding=embedding,
        limit=1,
    )

    assert len(results) == 1
    assert results[0]["text"] == "مستند عن الذكاء الاصطناعي"


def test_empty_query_embedding():
    with pytest.raises(ValueError):
        search_chunks([])


def test_store_and_search_with_metadata():
    embedding = [0.0, 1.0] + [0.0] * 382

    store_chunks(
        ["هذه معلومة من الصفحة الثانية"],
        [embedding],
        metadata=[
            {
                "filename": "sample.pdf",
                "page_number": 2,
            }
        ],
    )

    results = search_chunks(
        query_embedding=embedding,
        limit=1,
    )

    assert results[0]["filename"] == "sample.pdf"
    assert results[0]["page_number"] == 2