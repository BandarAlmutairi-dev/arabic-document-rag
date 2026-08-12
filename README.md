Arabic Document RAG

A production-ready Arabic Retrieval-Augmented Generation (RAG) API for asking questions about PDF and DOCX documents.

The system extracts document text, splits it into chunks, generates multilingual embeddings, stores them in a vector database, retrieves the most relevant context, and generates grounded Arabic answers with source references.

Live Demo

Swagger API:
https://arabic-document-rag-production.up.railway.app/docs

Health Check:
https://arabic-document-rag-production.up.railway.app/health

Features

* Arabic document question answering
* PDF and DOCX support
* Text extraction with source metadata
* Automatic text chunking
* Multilingual embeddings
* Semantic vector search
* Retrieval-Augmented Generation (RAG)
* Source citations in generated answers
* Persistent Qdrant vector storage
* FastAPI REST API
* Docker support
* Automated CI with GitHub Actions
* Production deployment on Railway

Architecture

Document
   ↓
PDF / DOCX Parser
   ↓
Text Chunking
   ↓
Multilingual Embeddings
   ↓
Qdrant Vector Database
   ↓
Semantic Retrieval
   ↓
Relevant Context
   ↓
OpenAI API
   ↓
Grounded Arabic Answer + Sources

API Endpoints

Method	Endpoint	Description
GET	/	API status
GET	/health	Health check
POST	/documents/upload	Upload and index PDF/DOCX
POST	/ask	Ask questions about indexed documents

Example

Request

{
  "question": "ما هي عاصمة المملكة العربية السعودية؟",
  "limit": 3
}

Response

{
  "answer": "عاصمة المملكة العربية السعودية هي الرياض. [Source 1]",
  "sources": [
    {
      "source_id": 1,
      "filename": "document.docx",
      "page_number": null,
      "paragraph_number": 1,
      "score": 0.89
    }
  ]
}

Tech Stack

* Python 3.11
* FastAPI
* OpenAI API
* Sentence Transformers
* intfloat/multilingual-e5-small
* Qdrant
* PyPDF
* python-docx
* Pytest
* Docker
* GitHub Actions
* Railway

Local Setup

Clone the repository:

git clone https://github.com/BandarAlmutairi-dev/arabic-document-rag.git
cd arabic-document-rag

Create a virtual environment and install dependencies:

python -m venv .venv
pip install -r requirements.txt

Create a .env file:

OPENAI_API_KEY=your_api_key_here

Run the API:

python -m uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/docs

Docker

Build the image:

docker build -t arabic-document-rag .

Run the container:

docker run --rm \
  --name arabic-document-rag \
  -p 8000:8000 \
  --env-file .env \
  arabic-document-rag

Tests

Run the complete test suite:

python -m pytest -q

The project includes tests for:

* API health
* Document parsing
* Text chunking
* Embeddings
* Vector storage
* Semantic search
* Retrieval
* RAG generation
* Document upload

Project Structure

arabic-document-rag/
├── app/
│   ├── main.py
│   ├── document_parser.py
│   ├── text_chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retrieval.py
│   └── rag_service.py
├── tests/
├── docs/
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

Deployment

The production API is deployed on Railway using Docker.

Persistent Qdrant data is stored using a Railway Volume mounted at:

/app/data/qdrant

This allows indexed documents to remain available after restarts and redeployments.

Security

The OpenAI API key is stored as an environment variable and is never committed to the repository.

The .env file and persistent local data are excluded from Git tracking.

Case Study

A detailed engineering case study is available in:

docs/CASE_STUDY.md

Status

Version: 1.0.0
Status: Production-ready

License

MIT License