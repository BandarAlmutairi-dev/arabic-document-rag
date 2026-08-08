from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_pages_from_pdf(file_bytes: bytes) -> list[dict[str, object]]:
    reader = PdfReader(BytesIO(file_bytes))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    return pages


def extract_paragraphs_from_docx(file_bytes: bytes) -> list[dict[str, object]]:
    document = Document(BytesIO(file_bytes))

    paragraphs = []

    for paragraph_number, paragraph in enumerate(
        document.paragraphs,
        start=1,
    ):
        text = paragraph.text.strip()

        if text:
            paragraphs.append(
                {
                    "paragraph_number": paragraph_number,
                    "text": text,
                }
            )

    return paragraphs


def extract_text_from_pdf(file_bytes: bytes) -> str:
    pages = extract_pages_from_pdf(file_bytes)

    return "\n".join(
        str(page["text"])
        for page in pages
    )


def extract_text_from_docx(file_bytes: bytes) -> str:
    paragraphs = extract_paragraphs_from_docx(file_bytes)

    return "\n".join(
        str(paragraph["text"])
        for paragraph in paragraphs
    )