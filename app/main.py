from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

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
async def upload_document(file: UploadFile = File(...)) -> dict[str, str]:
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported",
        )

    return {
        "filename": filename,
        "content_type": file.content_type or "unknown",
        "status": "accepted",
    }