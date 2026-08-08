from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI

from app.retrieval import retrieve_relevant_chunks

load_dotenv()

MODEL_NAME = "gpt-5.6-terra"


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI()


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

        sources.append(
            {
                "source_id": index,
                "filename": result.get("filename"),
                "page_number": result.get("page_number"),
                "paragraph_number": result.get("paragraph_number"),
                "score": result.get("score"),
            }
        )

    return {
        "question": question,
        "context": "\n\n".join(context_parts),
        "sources": sources,
    }


def generate_answer(
    question: str,
    limit: int = 3,
) -> dict[str, object]:
    rag = build_rag_context(question, limit)

    context = str(rag["context"]).strip()

    if not context:
        return {
            "answer": "لم أجد معلومات كافية في المستندات للإجابة.",
            "sources": [],
        }

    client = get_openai_client()

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=(
            "أجب باللغة العربية اعتمادًا فقط على السياق المقدم. "
            "لا تخترع معلومات غير موجودة في السياق. "
            "استخدم الاستشهادات مثل [Source 1] عند الاستناد إلى مصدر."
        ),
        input=(
            f"السؤال:\n{question}\n\n"
            f"السياق:\n{context}"
        ),
    )

    return {
        "answer": response.output_text.strip(),
        "sources": rag["sources"],
    }