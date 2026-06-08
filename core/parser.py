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
    text_parts = []
    for page in doc:
        page_text = page.get_text()
        if page_text.strip():
            text_parts.append(page_text)
        else:
            images = page.get_images(full=True)
            for img in images:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha > 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                img_bytes = pix.tobytes("png")
                ocr_text = _ocr_bytes(img_bytes)
                if ocr_text:
                    text_parts.append(ocr_text)
    doc.close()
    return "\n".join(text_parts).strip()


def _ocr_bytes(img_bytes: bytes) -> str:
    try:
        import pytesseract
        from PIL import Image
        import io
        return pytesseract.image_to_string(Image.open(io.BytesIO(img_bytes)))
    except ImportError:
        return ""


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
