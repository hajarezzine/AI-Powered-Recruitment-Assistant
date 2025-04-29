import PyPDF2
from utils.config import roles

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def analyze_resume(pdf_file, role_key):
    resume_text = extract_text_from_pdf(pdf_file).lower()
    required_keywords = roles[role_key]
    found_keywords = [kw for kw in required_keywords if kw in resume_text]

    if len(found_keywords) >= len(required_keywords) // 2:
        return {
            "status": "selected",
            "message": f"✅ Selected! Matched skills: {found_keywords}"
        }
    else:
        return {
            "status": "rejected",
            "message": f"❌ Rejected. Found only: {found_keywords}"
        }
