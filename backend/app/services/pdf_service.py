import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> dict:
    doc = fitz.open(file_path)
    extracted_text = ""
    for page in doc:
        extracted_text += page.get_text()
    
    page_count = doc.page_count  # moved before close
    doc.close()
    
    word_count = len(extracted_text.split())
    
    return {
        "text": extracted_text.strip(),  # changed key to "text" to match frontend
        "page_count": page_count,
        "word_count": word_count
    }