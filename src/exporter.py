# Functions to export tailored resume
from docx import Document

def save_to_docx(text: str, output_path: str):
    """
    Save text into Word file.
    """
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(output_path)
