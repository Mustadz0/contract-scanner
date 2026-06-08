import os
import re
from pathlib import Path
from typing import Optional


def extract_text(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if ext == ".txt":
        return file_path.read_text("utf-8", errors="replace")
    elif ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return _extract_docx(file_path)
    else:
        raise ValueError(f"Unsupported format: {ext}. Use .txt, .pdf, or .docx")


def _extract_pdf(path: Path) -> str:
    try:
        import fitz
    except ImportError:
        raise ImportError("Install PyMuPDF: pip install PyMuPDF")
    doc = fitz.open(str(path))
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text.strip()


def _extract_docx(path: Path) -> str:
    try:
        from docx import Document
    except ImportError:
        raise ImportError("Install python-docx: pip install python-docx")
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs).strip()


def extract_clauses(text: str) -> list:
    clauses = []
    lines = text.split("\n")
    current = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^\d+[\.\)]", stripped) or re.match(r"^[A-Z][A-Z\s]{2,}", stripped):
            if current:
                clauses.append(" ".join(current))
            current = [stripped]
        elif stripped:
            current.append(stripped)
    if current:
        clauses.append(" ".join(current))
    return [c for c in clauses if len(c) > 20]
