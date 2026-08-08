from unittest.mock import Mock, patch

from app.rag_service import build_rag_context, generate_answer


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
    assert len(result["sources"]) == 2
    assert result["sources"][0]["filename"] == "sample.pdf"


def test_generate_answer():
    fake_rag = {
        "question": "ما محتوى المستند؟",
        "context": "[Source 1]\nهذه معلومة من المستند",
        "sources": [
            {
                "source_id": 1,
                "filename": "sample.pdf",
                "page_number": 2,
                "paragraph_number": None,
                "score": 0.95,
            }
        ],
    }

    mock_response = Mock()
    mock_response.output_text = "الإجابة موجودة في المستند [Source 1]"

    mock_client = Mock()
    mock_client.responses.create.return_value = mock_response

    with patch("app.rag_service.build_rag_context", return_value=fake_rag):
        with patch(
            "app.rag_service.get_openai_client",
            return_value=mock_client,
        ):
            result = generate_answer("ما محتوى المستند؟")

    assert result["answer"] == "الإجابة موجودة في المستند [Source 1]"
    assert len(result["sources"]) == 1


def test_generate_answer_without_context():
    fake_rag = {
        "question": "سؤال",
        "context": "",
        "sources": [],
    }

    with patch("app.rag_service.build_rag_context", return_value=fake_rag):
        result = generate_answer("سؤال")

    assert result["sources"] == []
    assert "لم أجد معلومات كافية" in result["answer"]