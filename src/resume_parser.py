"""
Resume parsing utilities.

Supports PDF, DOCX and plain text resumes. Keeps parsing logic isolated
from scoring/extraction logic so each file swap (e.g. adding OCR for
scanned resumes) doesn't ripple through the rest of the app.
"""

import io
import re

import pdfplumber
from docx import Document


def parse_pdf(file_obj) -> str:
    """Extract text from a PDF file-like object."""
    text_chunks = []
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)


def parse_docx(file_obj) -> str:
    """Extract text from a DOCX file-like object."""
    document = Document(file_obj)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def parse_txt(file_obj) -> str:
    """Extract text from a plain text file-like object."""
    raw = file_obj.read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="ignore")
    return raw


def parse_resume(file_obj, filename: str) -> str:
    """
    Dispatch to the right parser based on file extension.
    file_obj must be a file-like object opened in binary mode (or a
    Streamlit UploadedFile, which behaves the same way).
    """
    filename_lower = filename.lower()
    if filename_lower.endswith(".pdf"):
        return parse_pdf(file_obj)
    elif filename_lower.endswith(".docx"):
        return parse_docx(file_obj)
    elif filename_lower.endswith(".txt"):
        return parse_txt(file_obj)
    else:
        raise ValueError(f"Unsupported file type: {filename}")


def clean_text(text: str) -> str:
    """Normalize whitespace and strip odd characters picked up by PDF parsing."""
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text
