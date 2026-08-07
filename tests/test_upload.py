from io import BytesIO

from docx import Document
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app

client = TestClient(app)


def create_pdf() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)

    buffer = BytesIO()
    writer.write(buffer)

    return buffer.getvalue()


def create_docx() -> bytes:
    document = Document()
    document.add_paragraph("مرحبا بالعالم")

    buffer = BytesIO()
    document.save(buffer)

    return buffer.getvalue()


def test_upload_pdf():
    response = client.post(
        "/documents/upload",
        files={"file": ("sample.pdf", create_pdf(), "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.pdf"
    assert response.json()["status"] == "processed"


def test_reject_unsupported_file():
    response = client.post(
        "/documents/upload",
        files={"file": ("sample.txt", b"text", "text/plain")},
    )

    assert response.status_code == 400


def test_upload_docx():
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.docx",
                create_docx(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.docx"
    assert response.json()["status"] == "processed"
    assert "مرحبا بالعالم" in response.json()["text"]