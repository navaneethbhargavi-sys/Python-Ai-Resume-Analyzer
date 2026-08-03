SECTIONS = {
    "Skills": {
        "headings": [
            "Skills",
            "Technical Skills",
            "Core Competencies",
            "Technologies"
        ],
        "score": 20
    },
    "Education": {
        "headings": [
            "Education",
            "Academic Background",
            "Academic Qualifications",
            "Educational Qualifications",
            "Qualifications"
        ],
        "score": 10
    },
    "Projects": {
        "headings": [
            "Projects",
            "Personal Projects",
            "Academic Projects",
            "Key Projects"
        ],
        "score": 20
    },
    "Experience": {
        "headings": [
            "Experience",
            "Work Experience",
            "Professional Experience",
            "Internship Experience",
            "Internships",
            "Employment History",
            "Work History"
        ],
        "score": 20
    }
}

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
    
    for section in SECTIONS:
        update_report(
            report,
            resume_text,
            SECTIONS[section]["headings"],
            section,
            SECTIONS[section]["score"]
        )

    return report