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

ACTION_VERBS = [
    "Built",
    "Developed",
    "Created",
    "Implemented",
    "Designed",
    "Engineered",
    "Optimized",
    "Automated",
    "Integrated",
    "Led"
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
    
    for technical_skill in TECHNICAL_SKILLS:
        if technical_skill.lower() in resume_text:
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

def has_link(resume_text, domain):
    return domain in resume_text

def count_action_verbs(resume_text):
    verb_count = 0
    
    for action_verb in ACTION_VERBS:
        if action_verb.lower() in resume_text:
            verb_count += 1
    return verb_count  

def add_suggestions(report, text):
    report["suggestions"].append(text)        
    
def update_boolean_check(resume_text, report, link_key, link, result):
    report[link_key] = has_link(resume_text, link)
    if report[link_key]:
        report["strengths"].append(f"{result} found")
    else:
        add_suggestions(report, result)

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
        report["strengths"].append(f"{section} section found")
    else:
        add_suggestions(report, f"Add {section} to improve your ATS score")
        report["missing_sections"].append(section)
        
def analyze_resume(resume_text):
    report = {
        "score": 0,
        "strengths": [],
        "missing_sections": [],
        "technical_skills": [],
        "technical_skills_count": 0,
        "github_found": False,
        "linkedin_found": False,
        "email_found": False,
        "phone_num_found": False,
        "action_verbs_count": 0,
        "suggestions": []
    }
    
    lowered_resume_text = resume_text.lower()
    
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
    
    report["technical_skills"] = find_technical_skills(lowered_resume_text)
    
    report["technical_skills_count"] = len(report["technical_skills"])
    technical_skills_count = report["technical_skills_count"]
    
    if technical_skills_count == 0:
        add_suggestions(report, "Technical Skills")
    
    technical_score = technical_skills_score(technical_skills_count)
    
    report["score"] += technical_score
    report["score_breakdown"]["Technical Skills"] = {
        "score": technical_score,
        "max_score": MAX_TECH_SCORE
    }
    
    update_boolean_check(lowered_resume_text, report, "github_found", "github.com", "GitHub Links")
    
    update_boolean_check(lowered_resume_text, report, "linkedin_found", "linkedin.com", "Linkedin Links")
     
    update_boolean_check(lowered_resume_text, report, "email_found", "@", "Email")   
    
    update_boolean_check(lowered_resume_text, report, "phone_num_found", "+91", "Phone number")  
    
    report["action_verbs_count"] = count_action_verbs(lowered_resume_text)
    verb_count = report["action_verbs_count"]
    if verb_count == 0:
        add_suggestions(report, "Action verbs")
    elif 1 <= verb_count < 4:
        report["strengths"].append(f"Good use of action verbs ({verb_count} detected)")
    elif 4 <= verb_count < 8:
        report["strengths"].append(f"Strong use of action verbs ({verb_count} detected)")
    elif verb_count >= 8:
        report["strengths"].append(f"Excellent use of action verbs ({verb_count} detected)")
      
    return report