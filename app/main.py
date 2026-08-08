from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.document_parser import (
    extract_pages_from_pdf,
    extract_paragraphs_from_docx,
)
from app.embeddings import embed_documents
from app.text_chunker import split_text
from app.vector_store import store_chunks

app = FastAPI(
    title="Arabic Document RAG",
    version="0.1.0",
)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Arabic Document RAG API is running"
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy"
    }


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, object]:
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported",
        )

    file_bytes = await file.read()

    try:
        chunks: list[str] = []
        metadata: list[dict[str, object]] = []
        text_parts: list[str] = []

        if extension == ".pdf":
            pages = extract_pages_from_pdf(file_bytes)

            for page in pages:
                page_text = str(page["text"])
                text_parts.append(page_text)

                page_chunks = split_text(page_text)

                chunks.extend(page_chunks)

                metadata.extend(
                    {
                        "filename": filename,
                        "page_number": page["page_number"],
                    }
                    for _ in page_chunks
                )

        else:
            paragraphs = extract_paragraphs_from_docx(file_bytes)

            for paragraph in paragraphs:
                paragraph_text = str(paragraph["text"])
                text_parts.append(paragraph_text)

                paragraph_chunks = split_text(paragraph_text)

                chunks.extend(paragraph_chunks)

                metadata.extend(
                    {
                        "filename": filename,
                        "paragraph_number": paragraph["paragraph_number"],
                    }
                    for _ in paragraph_chunks
                )

        embeddings = embed_documents(chunks)

        store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            metadata=metadata,
        )

        text = "\n".join(text_parts)

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Unable to process document",
        ) from exc

    return {
        "filename": filename,
        "content_type": file.content_type or "unknown",
        "status": "processed",
        "text": text,
        "chunks": chunks,
        "chunk_count": len(chunks),
    }