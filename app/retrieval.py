from app.embeddings import embed_query
from app.vector_store import search_chunks


def retrieve_relevant_chunks(
    query: str,
    limit: int = 3,
) -> list[dict[str, object]]:
    query_embedding = embed_query(query)

    return search_chunks(
        query_embedding=query_embedding,
        limit=limit,
    )