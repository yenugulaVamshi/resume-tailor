# Functions to rewrite resume sections with LLM
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def rewrite_section(resume_text: str, prompt: str) -> str:
    """
    Uses Gemini to rewrite part of resume based on user prompt.
    """
    full_prompt = f"""
    You are a professional resume writer.
    Resume section:
    {resume_text}

    Instruction:
    {prompt}

    Rewrite clearly, ATS-friendly, and professional.
    """
    response = model.generate_content(full_prompt)
    return response.text.strip()
