SECTIONS = {
    "Skills": {
        "headings": [
            "Skills",
            "Technical Skills",
            "Core Competencies",
            "Technologies"
        ],
        "max_score": 15
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
        "max_score": 15
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
        "max_score": 15
    },
    "Summary": {
        "headings": [
            "Summary",
            "Professional Summary",
            "Profile",
            "Career Objective",
            "Objective",
            "Professional Profile",
            "About Me",
            "Personal Profile"
        ],
        "max_score": 10
    },
    "Certifications": {
        "headings": [
            "Certifications",
            "Certification",
            "Certificates",
            "Courses",
            "Online Courses",
            "Professional Development",
            "Licenses"
        ],
        "max_score": 5
    }
}

MAX_TECH_SCORE = 20
MAX_GITHUB_SCORE = 5
MAX_LINKEDIN_SCORE = 5
MAX_EMAIL_SCORE = 3
MAX_PHONE_SCORE = 2

ADDITIONAL_SCORES = {
    "Technical Skills": MAX_TECH_SCORE
}

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

LINK_CHECKS={
    "GitHub Links": {
        "domain": "github.com",
        "report_key": "github_found",
        "score": 5
    },
    "Linkedin Links": {
        "domain": "linkedin.com",
        "report_key": "linkedin_found",
        "score": 3
    },
    "Email": {
        "domain": "@",
        "report_key": "email_found",
        "score": 1
    },
    "Phone number": {
        "domain": "+91",
        "report_key": "phone_number_found",
        "score": 1
    },
}

BEGINNER_SKILL_SCORE = 5
INTERMEDIATE_SKILL_SCORE = 10
ADVANCED_SKILL_SCORE = 20

def has_section(resume_text, headings):
    for heading in headings:
        if heading in resume_text:
            return True
    return False

def extract_section_text(resume_text, headings):
    for heading in headings:
        if heading in resume_text:
            start_index = resume_text.index(heading)
            end_index = len(resume_text)
                
    return ""
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

def count_numbers(resume_text):
    count = 0
    inside_number = False
    
    for element in resume_text:
        if element.isdigit():
            if not inside_number:
                count += 1
            inside_number = True
        else: 
            inside_number = False
            
    return count

def add_suggestions(report, item):
    report["suggestions"].append(f"Add {item} to improve your ATS score")        

def initialize_score(report, key, max_score):
    report["score_breakdown"][key] = {
        "score": 0,
        "max_score": max_score
    }

def evaluate_link(resume_text, report, link_key, link, result, score):
    initialize_score(report, result, score)
    
    found = has_link(resume_text, link) 
    report[link_key] = found
    
    if found:
        report["score"] += score
        report["score_breakdown"][result]["score"] = score
        report["strengths"].append(f"{result} found")
    else:
        add_suggestions(report, result)

def update_section(
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
        add_suggestions(report, section)
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
        "phone_number_found": False,
        "action_verbs_count": 0,
        "word_count": 0,
        "suggestions": []
    }
    
    resume_lower = resume_text.lower()
    
    report["score_breakdown"] = {}
            
    for section in SECTIONS:
        initialize_score(report, section, SECTIONS[section]["max_score"])
    
    for key, max_score in ADDITIONAL_SCORES.items():
        initialize_score(report, key, max_score)

    for section in SECTIONS:
        update_section(
            report,
            resume_text,
            SECTIONS[section]["headings"],
            section,
            SECTIONS[section]["max_score"]
        )
    
    report["technical_skills"] = find_technical_skills(resume_lower)
    
    technical_skills_count = len(report["technical_skills"])
    report["technical_skills_count"] = technical_skills_count
    
    if technical_skills_count == 0:
        add_suggestions(report, "Technical Skills")
    
    technical_score = technical_skills_score(technical_skills_count)
    
    report["score"] += technical_score
    report["score_breakdown"]["Technical Skills"]["score"] = technical_score
    
    for label, details in LINK_CHECKS.items():
        evaluate_link(
            resume_lower,
            report,
            details["report_key"],
            details["domain"],
            label,
            details["score"]
        )
    
    verb_count = count_action_verbs(resume_lower)
    report["action_verbs_count"] = verb_count
    if verb_count == 0:
        add_suggestions(report, "Action verbs")
    elif 1 <= verb_count < 4:
        report["strengths"].append(f"Good use of action verbs ({verb_count} detected)")
    elif 4 <= verb_count < 8:
        report["strengths"].append(f"Strong use of action verbs ({verb_count} detected)")
    elif verb_count >= 8:
        report["strengths"].append(f"Excellent use of action verbs ({verb_count} detected)")
        
    report["numbers_count"] = count_numbers(resume_text)
    
    report["word_count"] = len(resume_text.split())
    
    projects_text = extract_section_text(
        resume_text,
        SECTIONS["Projects"]["headings"]
    )
    report["projects_text"] = projects_text
      
    return report