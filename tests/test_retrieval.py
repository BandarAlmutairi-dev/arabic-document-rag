from unittest.mock import patch

from app.retrieval import retrieve_relevant_chunks


def test_retrieve_relevant_chunks():
    fake_embedding = [0.1] * 384
    fake_results = [
        {
            "text": "هذا النص مرتبط بالسؤال",
            "score": 0.95,
        }
    ]

    with patch("app.retrieval.embed_query", return_value=fake_embedding):
        with patch("app.retrieval.search_chunks", return_value=fake_results):
            results = retrieve_relevant_chunks(
                "ما محتوى المستند؟",
                limit=1,
            )

    assert len(results) == 1
    assert results[0]["text"] == "هذا النص مرتبط بالسؤال"
    assert results[0]["score"] == 0.95