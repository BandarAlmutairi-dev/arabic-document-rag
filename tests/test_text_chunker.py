import pytest

from app.text_chunker import split_text


def test_split_text_into_chunks():
    text = "واحد اثنان ثلاثة أربعة خمسة ستة سبعة ثمانية تسعة عشرة"

    chunks = split_text(text, chunk_size=4, overlap=1)

    assert chunks == [
        "واحد اثنان ثلاثة أربعة",
        "أربعة خمسة ستة سبعة",
        "سبعة ثمانية تسعة عشرة",
    ]


def test_empty_text_returns_empty_list():
    assert split_text("") == []


def test_invalid_overlap_raises_error():
    with pytest.raises(ValueError):
        split_text("نص تجريبي", chunk_size=5, overlap=5)