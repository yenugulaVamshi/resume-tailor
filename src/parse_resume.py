import os
import fitz  # PyMuPDF
import docx2txt
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_raw_text(file_path: str) -> str:
    """
    Extract raw text from PDF or DOCX without formatting.
    """
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")

def parse_resume_with_gemini(file_path: str) -> str:
    """
    Use Gemini to parse resume into structured JSON.
    """
    raw_text = extract_raw_text(file_path)
    
    prompt = f"""
    You are an expert ATS resume parser.
    Convert the following raw resume text into clean structured JSON with keys:
    Summary, Skills, Experience, Education, Projects, Certifications.

    --- Resume Raw Text ---
    {raw_text}
    """
    
    response = model.generate_content(prompt)
    return response.text
