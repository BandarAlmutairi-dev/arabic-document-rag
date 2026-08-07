from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_pdf():
    response = client.post(
        "/documents/upload",
        files={"file": ("sample.pdf", b"fake pdf content", "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.pdf"
    assert response.json()["status"] == "accepted"


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
                b"fake docx content",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.docx"
    assert response.json()["status"] == "accepted"