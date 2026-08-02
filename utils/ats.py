SKILLS_HEADINGS = [
    "Skills",
    "Technical Skills",
    "Core Competencies",
    "Technologies"
]

EDUCATION_HEADINGS = [
    "Education",
    "Academic Background",
    "Academic Qualifications",
    "Educational Qualifications",
    "Qualifications"
]

PROJECT_HEADINGS = [
    "Projects",
    "Personal Projects",
    "Academic Projects",
    "Key Projects"
]

SKILLS_SCORE = 20
EDUCATION_SCORE = 20
PROJECTS_SCORE = 20

def has_skills_section(resume_text):
    for heading in SKILLS_HEADINGS:
        if heading in resume_text:
            return True
    return False

def has_education_section(resume_text):
    for heading in EDUCATION_HEADINGS:
        if heading in resume_text:
            return True
    return False

def has_projects_section(resume_text):
    for heading in PROJECT_HEADINGS:
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
    
    if has_skills_section(resume_text):
        report["score"] += SKILLS_SCORE
        report["strengths"].append("Skills section found")
    else:
        report["weaknesses"].append("Skills section missing")
        report["missing_sections"].append("Skills")
    
    if has_education_section(resume_text):
        report["score"] += EDUCATION_SCORE
        report["strengths"].append("Education section found")
    else:
        report["weaknesses"].append("Education section missing")
        report["missing_sections"].append("Education")
        
    if has_projects_section(resume_text):
        report["score"] += PROJECTS_SCORE
        report["strengths"].append("Projects section found")
    else:
        report["weaknesses"].append("Projects section missing")    
        report["missing_sections"].append("Projects")
    return report