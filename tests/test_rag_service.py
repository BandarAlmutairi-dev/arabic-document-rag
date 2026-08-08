from unittest.mock import patch

from app.rag_service import build_rag_context


def test_build_rag_context():
    fake_results = [
        {
            "text": "المعلومة الأولى",
            "filename": "sample.pdf",
            "page_number": 2,
            "paragraph_number": None,
            "score": 0.95,
        },
        {
            "text": "المعلومة الثانية",
            "filename": "sample.docx",
            "page_number": None,
            "paragraph_number": 4,
            "score": 0.90,
        },
    ]

    with patch(
        "app.rag_service.retrieve_relevant_chunks",
        return_value=fake_results,
    ):
        result = build_rag_context(
            "ما محتوى المستند؟",
            limit=2,
        )

    assert result["question"] == "ما محتوى المستند؟"
    assert "[Source 1]" in result["context"]
    assert "المعلومة الأولى" in result["context"]
    assert len(result["sources"]) == 2
    assert result["sources"][0]["filename"] == "sample.pdf"
    assert result["sources"][0]["page_number"] == 2
    assert result["sources"][1]["paragraph_number"] == 4