import re

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

LINK_CHECKS = {
    "GitHub Links": {
        "pattern": r"github\.com/[A-Za-z0-9_-]+",
        "report_key": "github_found",
        "score": 5
    },
    "Linkedin Links": {
        "pattern": r"linkedin\.com/(?:in|pub)/[A-Za-z0-9_-]+",
        "report_key": "linkedin_found",
        "score": 3
    },
    "Email": {
        "pattern": r"[A-Za-z0-9._]+@[A-Za-z0-9.-]+\.[A-Za-z]+",
        "report_key": "email_found",
        "score": 1
    },
    "Phone number": {
        "pattern": r"\+91[\s-]?[6-9]\d{9}",
        "report_key": "phone_number_found",
        "score": 1
    }
}

BEGINNER_SKILL_SCORE = 5
INTERMEDIATE_SKILL_SCORE = 10
ADVANCED_SKILL_SCORE = 20

def has_section(resume_text, headings):
    for heading in headings:
        pattern = rf"\b{heading}\b"
        
        if re.search(pattern, resume_text, re.IGNORECASE):
            return True
    return False

def has_link(resume_text, pattern):
    return bool(re.search(pattern, resume_text, re.IGNORECASE))

# TODO:
# Improve technical skill matching to avoid partial matches
# (e.g. "C" matching "C++" thru the `in` logic)
# Fixed
def find_technical_skills(resume_text):
    skills_list = []
    
    # for technical_skill in TECHNICAL_SKILLS:
    #     if technical_skill.lower() in resume_text:
    #         skills_list.append(technical_skill)
    for technical_skill in TECHNICAL_SKILLS:
        pattern = rf"(?<![A-Za-z0-9]){re.escape(technical_skill)}(?![A-Za-z0-9])"
        
        if re.search(pattern, resume_text, re.IGNORECASE):
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
    
def technical_skills_rating(tech_count):
    if tech_count == 0:
        return "None"
    elif 1 <= tech_count <= 3:
        return "Weak"
    elif 4 <= tech_count <= 7:
        return "Good"
    elif tech_count >= 8:
        return "Strong"
    
def add_tech_skills_feedback(report, tech_rating):
    if tech_rating == "None":
        report["suggestions"].append("Add technical skills like Python, SQL, Git, etc")
    elif tech_rating == "Weak":
        report["suggestions"].append("Include more skills like Python, SQL, Git, etc")
    elif tech_rating in ["Good", "Strong"]:
        report["strengths"].append(f"{tech_rating} use of technical skills")
    
def extract_section_text(resume_text, headings):
    for heading in headings:
        if heading in resume_text:
            start_index = resume_text.index(heading)
            end_index = len(resume_text)
            
            for section in SECTIONS:
                for next_heading in SECTIONS[section]["headings"]:
                    next_index = resume_text.find(next_heading, start_index + 1)
                    if next_index == -1:
                        pass
                    elif next_index < end_index:
                        end_index = next_index
                        
            return resume_text[start_index: end_index]
        
        elif heading.upper() in resume_text:
            start_index = resume_text.index(heading.upper())
            end_index_upper = len(resume_text)
            
            for section in SECTIONS:
                for next_heading in SECTIONS[section]["headings"]:
                    next_index_upper = resume_text.find(next_heading.upper(), start_index + 1)
                    if next_index_upper == -1:
                        pass
                    elif next_index_upper < end_index_upper:
                        end_index_upper = next_index_upper
                   
            return resume_text[start_index: end_index_upper]
                
    return ""

def evaluate_section_length(word_count):
    if 0 < word_count <= 30:
        return "Too Short"
    elif 30 <= word_count <= 150:
        return "Good"
    elif word_count > 150:
        return "Too Long" 
    
def add_section_length_feedback(rating, report, section):
    if rating == "Too Short":
        report["suggestions"].append(f"Your {section} section may need more detail")
    elif rating == "Good":
        report["strengths"].append(f"Sufficient detail in your {section} section")
    elif rating == "Too Long":
        report["suggestions"].append(f"Consider making your {section} section more concise")

def count_action_verbs(resume_text):
    verb_count = 0
    
    for action_verb in ACTION_VERBS:
        if action_verb.lower() in resume_text:
            verb_count += 1
    return verb_count  

def evaluate_action_verbs(action_verbs_count):
    if action_verbs_count == 0:
        return "None"
    elif 1 <= action_verbs_count < 3:
        return "Weak"
    elif 3 <= action_verbs_count < 6:
        return "Good"
    elif action_verbs_count >= 6:
        return "Strong"

def add_action_verb_feedback(rating, report, section):
    if rating == "None":
        report["suggestions"].append(f"Add action verbs such as Built, Developed, Implemented, Designed, etc to your {section} section")
    elif rating == "Weak":
        report["suggestions"].append(f"Replace generic wording with stronger action verbs in your {section} section to make your achievements more impactful.")
    elif rating in ["Good", "Strong"]:
        report["strengths"].append(f"{rating} usage of action verbs in {section} section")

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

def evaluate_numbers(numbers_count):
    if numbers_count == 0:
        return "None"
    elif 1 <= numbers_count <= 2:
        return "Weak"
    elif 3 <= numbers_count <= 5:
        return "Good"
    elif numbers_count >= 6:
        return "Strong"

def add_number_feedback(rating, report):
    if rating == "None":
        report["suggestions"].append("Quantify your achievements by numbers.")
    elif rating == "Weak":
        report["suggestions"].append("Consider including more measurable results in your resume.")
    elif rating in ["Good", "Strong"]:
        report["strengths"].append(f"{rating} use of quantified information.")

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

def analyze_section(resume_text, report, section):
    lower_key = section.lower()
    result = {}
    
    text = extract_section_text(
        resume_text,
        SECTIONS[section]["headings"]
    )
    result[f"{lower_key}_text"] = text
    
    result[f"{lower_key}_word_count"] = len(text.split())
    result[f"{lower_key}_word_rating"] =  evaluate_section_length(result[f"{lower_key}_word_count"])
    add_section_length_feedback(
        result[f"{lower_key}_word_rating"], 
        report, 
        section
    )
    
    result[f"{lower_key}_action_verbs_count"] = count_action_verbs(text.lower())
    result[f"{lower_key}_action_verbs_rating"] = evaluate_action_verbs(result[f"{lower_key}_action_verbs_count"])
    add_action_verb_feedback(
        result[f"{lower_key}_action_verbs_rating"],
        report,
        section
    )
    
    return result

def analyze_resume(resume_text):
    report = {
        "score": 0,
        "strengths": [],
        "suggestions": [],
        "missing_sections": [],
        
        "technical_skills": [],
        "technical_skills_count": 0,
        "technical_skills_rating": "None",
        
        "github_found": False,
        "linkedin_found": False,
        "email_found": False,
        "phone_number_found": False,
        
        "action_verbs_count": 0,
        "projects_action_verbs_count": 0,
        "experience_action_verbs_count": 0,
        
        "projects_word_count": 0,
        "experience_word_count": 0,
        
        "projects_action_verbs_rating": "None",
        "experience_action_verbs_rating": "None",
        
        "projects_word_rating": "Too Short",
        "experience_word_rating": "Too Short",
        
        "word_count": 0,
        
        "numbers_count": 0,
        "numbers_rating": "None",
        
        "projects_text": "",
        "experience_text": "",
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
    
    report["technical_skills_rating"] = technical_skills_rating(technical_skills_count)
    add_tech_skills_feedback(report, report["technical_skills_rating"])
    
    for label, details in LINK_CHECKS.items():
        evaluate_link(
            resume_lower,
            report,
            details["report_key"],
            details["pattern"],
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
    report["numbers_rating"] = evaluate_numbers(report["numbers_count"])
    add_number_feedback(report["numbers_rating"], report)
    
    report["word_count"] = len(resume_text.split())
    
    analyzed_sections = []
    
    analyzed_sections.append(analyze_section(resume_text, report, "Projects"))
    analyzed_sections.append(analyze_section(resume_text,report, "Experience"))
    
    for analyzed_section in analyzed_sections:
        for key, value in analyzed_section.items():
            report[key] = value
    
    return report