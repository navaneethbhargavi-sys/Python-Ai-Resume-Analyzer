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

PROJECTS_HEADINGS = [
    "Projects",
    "Personal Projects",
    "Academic Projects",
    "Key Projects"
]

SKILLS_SCORE = 20
EDUCATION_SCORE = 20
PROJECTS_SCORE = 20

def has_section(resume_text, headings):
    for heading in headings:
        if heading in resume_text:
            return True
    return False

def update_report(report, resume_text, headings, section, score):
    if has_section(resume_text, headings):
        report["score"] += score
        report["strengths"].append(section)
    else:
        report["weaknesses"].append(section)
        report["missing_sections"].append(section)

def analyze_resume(resume_text):
    report = {
        "score": 0,
        "strengths": [],
        "weaknesses": [],
        "missing_sections": []
    }
    
    update_report(
        report,
        resume_text,
        SKILLS_HEADINGS,
        "Skills",
        SKILLS_SCORE
    )
    
    update_report(
        report,
        resume_text,
        EDUCATION_HEADINGS,
        "Education",
        EDUCATION_SCORE
    )
        
    update_report(
        report,
        resume_text,
        PROJECTS_HEADINGS,
        "Projects",
        PROJECTS_SCORE
    )
    return report