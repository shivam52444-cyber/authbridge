# utils/parser.py
import fitz  # PyMuPDF

def extract_text(file):
    # Case 1: file path (string)
    if isinstance(file, str):
        doc = fitz.open(file)
    
    # Case 2: file-like object (Streamlit upload)
    else:
        doc = fitz.open(stream=file.read(), filetype="pdf")
    
    pages = []
    
    for page in doc:
        page_text = page.get_text("text")
        if page_text:
            pages.append(page_text)
    
    return "\n".join(pages)
