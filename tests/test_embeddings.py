from unittest.mock import Mock, patch

import numpy as np
import pytest

from app.embeddings import embed_documents, embed_query


def test_embed_documents():
    mock_model = Mock()
    mock_model.encode.return_value = np.array(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]
    )

    with patch("app.embeddings.get_embedding_model", return_value=mock_model):
        embeddings = embed_documents(["نص عربي", "مستند آخر"])

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 3


def test_empty_documents():
    assert embed_documents([]) == []


def test_embed_query():
    mock_model = Mock()
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])

    with patch("app.embeddings.get_embedding_model", return_value=mock_model):
        embedding = embed_query("ما محتوى المستند؟")

    assert len(embedding) == 3


def test_empty_query_raises_error():
    with pytest.raises(ValueError):
        embed_query("")