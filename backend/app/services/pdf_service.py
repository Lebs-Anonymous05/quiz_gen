import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> dict:
    """
    Extract text content from a PDF file.

    Args:
        file_path: Path to the uploaded PDF file

    Returns:
        Dictionary with extracted text, page count, and word count
    """
    doc = fitz.open(file_path)

    extracted_text = ""
    for page in doc:
        extracted_text += page.get_text()

    doc.close()

    word_count = len(extracted_text.split())
    page_count = doc.page_count

    return {
        "extracted_text": extracted_text.strip(),
        "page_count": page_count,
        "word_count": word_count
    }