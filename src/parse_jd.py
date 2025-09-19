# Functions to parse job description
def read_job_description(file_path: str = None, jd_text: str = None) -> str:
    """
    Reads job description from a text file or direct input.
    """
    if jd_text:
        return jd_text.strip()
    
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    raise ValueError("Provide either a JD text or JD file path.")
