# Main pipeline orchestrator
from parse_resume import parse_resume_with_gemini
from parse_jd import read_job_description
from analyzer import analyze_resume_vs_jd
from rewrite_engine import rewrite_section
from exporter import save_to_docx

def run_pipeline(resume_path: str, jd_path: str, output_path: str):
    # Step 1: Read inputs
    resume_text = parse_resume_with_gemini(resume_path)
    jd_text = read_job_description(file_path=jd_path)

    # Step 2: Analyze
    analysis = analyze_resume_vs_jd(resume_text, jd_text)
    print("Match Score:", analysis["match_score"], "%")
    print("Missing Keywords:", analysis["missing_keywords"])

    # Step 3: Rewrite
    tailored_resume = rewrite_section(resume_text, f"Tailor this resume for job description: {jd_text}")

    # Step 4: Export
    save_to_docx(tailored_resume, output_path)
    print(f"✅ Tailored resume saved at {output_path}")

if __name__ == "__main__":
    run_pipeline("inputs/resume.pdf", "inputs/job_description.txt", "outputs/tailored_resume.docx")
