import sys, os
import streamlit as st

# --- Fix Python Path so src/ is discoverable ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parse_resume import parse_resume_with_gemini
from src.parse_jd import read_job_description
from src.analyzer import analyze_resume_vs_jd
from src.rewrite_engine import rewrite_section
from src.exporter import save_to_docx

st.title("AI Resume Tailor 🚀")

resume_file = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])
jd_text_input = st.text_area("Paste Job Description")
jd_file = st.file_uploader("Or upload JD (.txt)", type=["txt"])

resume_text, jd_text = "", ""

if resume_file:
    temp_path = "inputs/temp_resume." + resume_file.name.split(".")[-1]
    with open(temp_path, "wb") as f:
        f.write(resume_file.getbuffer())
    resume_text = parse_resume_with_gemini(temp_path)
    st.subheader("📄 Resume Preview (Editable)")
    resume_text = st.text_area("Resume", resume_text, height=300)

if jd_text_input or jd_file:
    if jd_file:
        temp_jd = "inputs/temp_jd.txt"
        with open(temp_jd, "wb") as f:
            f.write(jd_file.getbuffer())
        jd_text = read_job_description(file_path=temp_jd)
    else:
        jd_text = jd_text_input
    
    st.subheader("📄 Job Description Preview (Editable)")
    jd_text = st.text_area("Job Description", jd_text, height=300)

if resume_text and jd_text:
    if st.button("Analyze Match"):
        result = analyze_resume_vs_jd(resume_text, jd_text)
        st.write(f"✅ Match Score: {result['match_score']}%")
        st.write("❌ Missing Keywords:", ", ".join(result['missing_keywords']))

    user_prompt = st.text_input("Enter change prompt (e.g., 'Add Azure ML in skills')")
    if st.button("Apply Prompt Change"):
        updated_resume = rewrite_section(resume_text, user_prompt)
        st.text_area("Updated Resume", updated_resume, height=300)

    if st.button("Generate Tailored Resume"):
        tailored_resume = rewrite_section(resume_text, f"Tailor this resume for: {jd_text}")
        save_to_docx(tailored_resume, "outputs/tailored_resume.docx")
        st.success("🎉 Tailored Resume Generated!")
        with open("outputs/tailored_resume.docx", "rb") as f:
            st.download_button("⬇ Download Tailored Resume", f, file_name="tailored_resume.docx")
