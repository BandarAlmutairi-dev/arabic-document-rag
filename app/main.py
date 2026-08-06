from fastapi import FastAPI

app = FastAPI(
    title="Arabic Document RAG",
    version="0.1.0",
)


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