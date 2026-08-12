Arabic Document RAG — Case Study

Project Overview

Arabic Document RAG is an end-to-end Retrieval-Augmented Generation (RAG) system designed to answer questions from Arabic PDF and DOCX documents.

The project was built as a practical AI engineering portfolio project, with focus on document ingestion, semantic retrieval, source-aware answers, persistence, testing, containerization, CI, and production deployment.

Problem

Large language models can generate useful answers, but without grounding they may answer from general knowledge instead of the user’s documents.

The goal was to build a system that:

* Accepts Arabic PDF and DOCX files
* Extracts and indexes their content
* Retrieves only the most relevant passages
* Generates answers using retrieved document context
* Returns source metadata with the answer
* Rejects unrelated questions when document relevance is too low
* Preserves indexed data across restarts and redeployments

Solution

The system implements a complete RAG pipeline:

Document Upload
      ↓
PDF / DOCX Parsing
      ↓
Text Chunking
      ↓
Multilingual Embeddings
      ↓
Qdrant Vector Storage
      ↓
Semantic Retrieval
      ↓
Relevance Filtering
      ↓
OpenAI Generation
      ↓
Arabic Answer + Sources

Key Engineering Decisions

1. Arabic and Multilingual Embeddings

The project uses:

intfloat/multilingual-e5-small

Document chunks are embedded using the passage: prefix, while questions use the query: prefix.

Embeddings are normalized before vector search.

2. Source Metadata

The system preserves document source information.

For PDF files:

* Filename
* Page number

For DOCX files:

* Filename
* Paragraph number

This metadata is returned with generated answers.

3. Persistent Vector Storage

Qdrant is used as the vector database.

Local development stores Qdrant data under:

data/qdrant

In production, Railway uses a persistent Volume mounted at:

/app/data/qdrant

This allows indexed documents to survive application restarts and redeployments.

4. Relevance Filtering

Initial semantic search testing showed that unrelated questions could still receive moderate cosine similarity scores.

A minimum relevance threshold was therefore introduced:

0.75

Testing showed a clear distinction between relevant and unrelated queries in the current system.

Example:

Relevant question score: ~0.88–0.92
Unrelated question score: ~0.71

Questions below the threshold return:

لم أجد معلومات كافية في المستندات للإجابة.

5. Grounded Answer Generation

The language model is instructed to answer only from retrieved context and to cite sources using identifiers such as:

[Source 1]

If no relevant context is found, the OpenAI API is not used to fabricate an answer.

API Design

The application exposes a FastAPI REST API.

Health Check

GET /health

Upload Document

POST /documents/upload

Supported formats:

.pdf
.docx

Ask Question

POST /ask

Example request:

{
  "question": "ما هي عاصمة المملكة العربية السعودية؟",
  "limit": 3
}

Example response:

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

Testing

The project includes automated tests for:

* Health endpoint
* Document upload
* PDF parsing
* DOCX parsing
* Text chunking
* Embeddings
* Vector storage
* Semantic search
* Metadata handling
* Retrieval
* RAG context construction
* Answer generation

The final local test suite passed:

25 passed

Vector-store tests were isolated from production data by using an in-memory Qdrant instance during tests.

Docker

The application is containerized using Docker.

An early Docker build was much larger because PyTorch pulled GPU/CUDA-related dependencies.

The image was later optimized to use CPU-only PyTorch.

This reduced local Docker disk usage substantially while keeping the RAG system functional.

Continuous Integration

GitHub Actions automatically runs the test suite on:

* Pushes to main
* Pull requests targeting main

This ensures changes are validated before being treated as stable.

Production Deployment

The project is deployed on Railway.

Live Swagger API:

https://arabic-document-rag-production.up.railway.app/docs

Production deployment includes:

* Docker-based build
* Environment-based OpenAI API key
* Public HTTPS endpoint
* Persistent Railway Volume
* Automatic deployment from GitHub

Production Validation

The deployed application was manually validated end-to-end.

The following were tested successfully:

GET /health
POST /documents/upload
POST /ask

Persistence was also validated by:

1. Uploading a document
2. Redeploying the Railway service
3. Asking a question without re-uploading the document
4. Receiving the correct answer from the persisted Qdrant data

Challenges Solved

During development, several practical issues were identified and fixed:

* Scanned PDF with no extractable text
* OpenAI API quota error
* In-memory Qdrant losing data after restart
* Test data contaminating production vector storage
* Unrelated queries passing semantic search
* Docker image pulling unnecessary CUDA dependencies
* Windows Docker requiring WSL 2
* Railway environment variable configuration
* Railway persistent storage configuration

Current Capabilities

The current version can:

* Process Arabic DOCX documents
* Process text-based PDF documents
* Split text into chunks
* Create multilingual embeddings
* Store vectors persistently
* Perform semantic similarity search
* Reject low-relevance context
* Generate Arabic answers using RAG
* Return source metadata
* Run locally
* Run inside Docker
* Run automated tests in CI
* Run as a public production API

Limitations

The current version does not yet include:

* OCR for scanned/image-only PDFs
* Authentication
* User accounts
* Document deletion API
* Multi-tenant data isolation
* Web frontend
* Advanced reranking
* Hybrid keyword + vector search
* Streaming answers

These are potential future improvements rather than requirements for version 1.0.

Technologies

Python
FastAPI
OpenAI API
Sentence Transformers
Multilingual E5
Qdrant
PyPDF
python-docx
Pytest
Docker
GitHub Actions
Railway

Result

The project evolved from a local FastAPI experiment into a complete deployed Arabic RAG backend with semantic retrieval, persistence, automated testing, CI, containerization, source-aware generation, and a public production endpoint.

This demonstrates a practical end-to-end AI engineering workflow rather than only a model or notebook experiment.