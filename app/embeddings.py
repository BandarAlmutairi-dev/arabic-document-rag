from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-small"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_documents(texts: list[str]) -> list[list[float]]:
    clean_texts = [
        f"passage: {text.strip()}"
        for text in texts
        if text.strip()
    ]

    if not clean_texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        clean_texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    query = query.strip()

    if not query:
        raise ValueError("query must not be empty")

    model = get_embedding_model()

    embedding = model.encode(
        f"query: {query}",
        normalize_embeddings=True,
    )

    return embedding.tolist()