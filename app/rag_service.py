from app.retrieval import retrieve_relevant_chunks


def build_rag_context(
    question: str,
    limit: int = 3,
) -> dict[str, object]:
    results = retrieve_relevant_chunks(
        query=question,
        limit=limit,
    )

    context_parts: list[str] = []
    sources: list[dict[str, object]] = []

    for index, result in enumerate(results, start=1):
        text = str(result.get("text", "")).strip()

        if not text:
            continue

        context_parts.append(
            f"[Source {index}]\n{text}"
        )

        source = {
            "source_id": index,
            "filename": result.get("filename"),
            "page_number": result.get("page_number"),
            "paragraph_number": result.get("paragraph_number"),
            "score": result.get("score"),
        }

        sources.append(source)

    return {
        "question": question,
        "context": "\n\n".join(context_parts),
        "sources": sources,
    }