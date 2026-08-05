SECTIONS = {
    "Skills": {
        "headings": [
            "Skills",
            "Technical Skills",
            "Core Competencies",
            "Technologies"
        ],
        "max_score": 20
    },
    "Education": {
        "headings": [
            "Education",
            "Academic Background",
            "Academic Qualifications",
            "Educational Qualifications",
            "Qualifications"
        ],
        "max_score": 10
    },
    "Projects": {
        "headings": [
            "Projects",
            "Personal Projects",
            "Academic Projects",
            "Key Projects"
        ],
        "max_score": 20
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
        "max_score": 20
    }
}

MAX_TECH_SCORE = 20

TECHNICAL_SKILLS = [
    "Python",
    "C++",
    "C",
    "C#",
    "Java",
    "HTML",
    "CSS",
    "JavaScript",
    "TypeScript",
    "React",
    "MongoDB",
    "Express.js",
    "Node.js",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "Git",
    "GitHub",
    "GitHub Actions",
    "Vercel",
    "Docker",
    "Kubernetes",
    "AWS",
    "Power BI",
    "Flask",
    "Django",
    "Linux",
    "Ruby",
    "Rust",
    "Go",
    "Kotlin",
    "Php",
    "TensorFlow",
    "Redis"
]

BEGINNER_SKILL_SCORE = 5
INTERMEDIATE_SKILL_SCORE = 10
ADVANCED_SKILL_SCORE = 20

def has_section(resume_text, headings):
    for heading in headings:
        if heading in resume_text:
            return True
    return False

# TODO:
# Improve technical skill matching to avoid partial matches
# (e.g. "C" matching "C++" thru the `in` logic)
def find_technical_skills(resume_text):
    skills_list = []
    lowered_resume_text = resume_text.lower()
    
    for technical_skill in TECHNICAL_SKILLS:
        if technical_skill.lower() in lowered_resume_text:
            skills_list.append(technical_skill)
            
    return skills_list

def technical_skills_score(tech_skills_count):
    if tech_skills_count == 0:
        return 0
    if 1 <= tech_skills_count <= 3:
        return BEGINNER_SKILL_SCORE
    elif 4 <= tech_skills_count <= 7:
        return INTERMEDIATE_SKILL_SCORE
    elif tech_skills_count >= 8:
        return ADVANCED_SKILL_SCORE

def update_report(
    report, 
    resume_text, 
    headings, 
    section, 
    max_score
):  
    if has_section(resume_text, headings):
        report["score"] += max_score
        report["score_breakdown"][section]["score"] = max_score
        report["strengths"].append(section)
    else:
        report["weaknesses"].append(section)
        report["missing_sections"].append(section)
        
def analyze_resume(resume_text):
    report = {
        "score": 0,
        # "score_breakdown": {
        #     "Skills": {},
        #     "Education": {},
        #     "Projects": {},
        #     "Experience": {},
        #     "Technical Skills": {}              
        # },
        "strengths": [],
        "weaknesses": [],
        "missing_sections": [],
        "technical_skills": [],
        "technical_skills_count": 0,
        "suggestions": []
    }
    
    report["score_breakdown"] = {}
            
    for section in SECTIONS:
        report["score_breakdown"][section] = {
            "score": 0,
            "max_score": SECTIONS[section]["max_score"]
        }
    
    for section in SECTIONS:
        update_report(
            report,
            resume_text,
            SECTIONS[section]["headings"],
            section,
            SECTIONS[section]["max_score"]
        )
    
    report["technical_skills"] = find_technical_skills(resume_text)
    
    tech_skills_count = len(report["technical_skills"])
    report["technical_skills_count"] = tech_skills_count
    
    if tech_skills_count == 0:
        report["suggestions"].append("Technical Skills")
    
    technical_score = technical_skills_score(tech_skills_count)
    
    report["score"] += technical_score
    report["score_breakdown"]["Technical Skills"] = {
        "score": technical_score,
        "max_score": MAX_TECH_SCORE
    }
    
    return report