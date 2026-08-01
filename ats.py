SKILLS_HEADINGS = [
    "Skills",
    "Technical Skills",
    "Core Competencies",
    "Technologies"
]

def has_skills_section(resume_text):
    for heading in SKILLS_HEADINGS:
        if heading in resume_text:
            return True
    return False

def analyze_resume(resume_text):
    report = {
        "score": 0,
        "strengths": [],
        "weaknesses": [],
        "missing_sections": []
    }
    
    ##
    
    return report