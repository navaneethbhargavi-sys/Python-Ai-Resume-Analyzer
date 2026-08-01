from pypdf import PdfReader

def extract_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        
        if page_text: # handling none or empty page_text
            text += page_text
        
    return text