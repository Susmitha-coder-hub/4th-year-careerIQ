"""
backend/app/services/pdf_parser.py
Module 1: PDF Resume text extraction using pypdf.
Handles empty, corrupt, encrypted, and image-only PDFs with clear validation errors.
"""

import io
import re
from typing import Dict, Any, Tuple
from pypdf import PdfReader
from pypdf.errors import PdfReadError

def extract_basic_contact(text: str) -> Dict[str, Any]:
    """Extract candidate email, phone, and links using transparent regex."""
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    phone_match = re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text)
    linkedin_match = re.search(r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+', text, re.IGNORECASE)
    github_match = re.search(r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+', text, re.IGNORECASE)

    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "linkedin": linkedin_match.group(0) if linkedin_match else None,
        "github": github_match.group(0) if github_match else None,
    }

def parse_pdf_resume(file_bytes: bytes, filename: str, max_size_mb: int = 5) -> Dict[str, Any]:
    """
    Extract selectable text from a PDF resume using pypdf.
    Validates file size, encryption, corruption, and scanned PDFs.
    """
    # 1. Validate file size
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValueError(f"File size ({size_mb:.1f} MB) exceeds maximum allowed limit of {max_size_mb} MB.")

    if len(file_bytes) == 0:
        raise ValueError("Uploaded file is completely empty (0 bytes).")

    # 2. Parse PDF with pypdf
    try:
        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)
    except PdfReadError as e:
        raise ValueError(f"Corrupt or invalid PDF format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unable to read file: {str(e)}")

    # 3. Check for encryption
    if reader.is_encrypted:
        try:
            # Try decrypting with empty password
            decrypted = reader.decrypt("")
            if not decrypted:
                raise ValueError("PDF is password-protected or encrypted. Please remove password protection.")
        except Exception:
            raise ValueError("PDF is password-protected or encrypted. Please remove password protection.")

    # 4. Extract text across pages
    num_pages = len(reader.pages)
    if num_pages == 0:
        raise ValueError("The uploaded PDF contains 0 pages.")

    extracted_pages = []
    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        extracted_pages.append(page_text.strip())

    full_text = "\n\n".join(p for p in extracted_pages if p).strip()

    # 5. Check if selectable text exists (Graceful handling of scanned/image-only PDFs)
    if not full_text or len(full_text.split()) < 3:
        raise ValueError(
            "No selectable text found in the PDF. The document appears to be scanned or image-based. "
            "Optical Character Recognition (OCR) is not supported in this milestone. Please upload a PDF with selectable text."
        )

    contact_info = extract_basic_contact(full_text)
    word_count = len(full_text.split())

    return {
        "filename": filename,
        "page_count": num_pages,
        "word_count": word_count,
        "text": full_text,
        "text_preview": full_text[:600] + ("..." if len(full_text) > 600 else ""),
        "contact_info": contact_info,
    }
