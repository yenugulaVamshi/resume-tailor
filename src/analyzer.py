# Functions to analyze resume vs JD
import re

def analyze_resume_vs_jd(resume_text: str, jd_text: str) -> dict:
    """
    Compare resume vs JD to return match score & missing keywords.
    """
    resume_words = set(re.findall(r"\w+", resume_text.lower()))
    jd_words = set(re.findall(r"\w+", jd_text.lower()))

    stopwords = {"the","and","for","with","to","a","in","on","of"}
    filtered_jd = [w for w in jd_words if w not in stopwords]

    missing = [w for w in filtered_jd if w not in resume_words]
    match_count = len(filtered_jd) - len(missing)
    match_score = round((match_count / len(filtered_jd)) * 100, 2) if filtered_jd else 0

    return {
        "match_score": match_score,
        "missing_keywords": missing
    }
