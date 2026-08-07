from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.document_parser import (
    extract_text_from_docx,
    extract_text_from_pdf,
)
from app.text_chunker import split_text

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
        if extension == ".pdf":
            text = extract_text_from_pdf(file_bytes)
        else:
            text = extract_text_from_docx(file_bytes)

        chunks = split_text(text)

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