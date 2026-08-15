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
        "pattern": r"(?:\+91[\s-])?[6-9]\d{9}",
        "report_key": "phone_number_found",
        "score": 1
    }
}

EDUCATION_NUMBER_KEYWORDS = [
    "class",
    "percentage",
    "gpa",
    "cgpa"
]

EDUCATION_PATTERNS = [
    r"\b(?:X|XI|XII)(?:th)?\b"
]

PERCENTAGE_PATTERNS = [
    r"%"
]

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
        pattern = rf"^[ \t]*{re.escape(heading)}[ \t]*$"
        match = re.search(pattern, resume_text, re.IGNORECASE | re.MULTILINE)
        if match:
            start_index = match.start()
            end_index = len(resume_text)
            
            for section in SECTIONS:
                for next_heading in SECTIONS[section]["headings"]:
                    next_pattern = rf"^[ \t]*{re.escape(next_heading)}[ \t]*$"
                    next_match = re.search(next_pattern, resume_text[start_index + 1:], re.IGNORECASE | re.MULTILINE)
                    
                    if next_match is None:
                        continue
                    
                    next_index = start_index + 1 + next_match.start() 
                    if next_index < end_index:
                        end_index = next_index
     
            return resume_text[start_index: end_index]
                
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

def find_action_verbs(resume_text):
    freq_dict = {}
    
    for action_verb in ACTION_VERBS:
        pattern = rf"\b{re.escape(action_verb)}\b"
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        
        if matches: 
            freq_dict[action_verb] = {}
            freq_dict[action_verb]["frequency"] = len(matches)
            freq_dict[action_verb]["rating"] = "None"
    return freq_dict

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
        
def evaluate_action_verbs_frequency(verb_frequency):
    if verb_frequency in [1, 2]:
        return "Optimum"
    elif verb_frequency == 3:
        return "Worth varying"
    elif verb_frequency >= 4:
        return "Overused"

def add_action_verb_freq_feedback(rating, report, verb, frequency, section):
    if rating == "None":
        pass
    elif rating == "Optimum":
        report["strengths"].append(f"Optimum frequency maintained for action verbs for your {section} section")
    elif rating == "Worth Varying":
        report["suggestions"].append(f'{section}: "{verb}" is used {frequency} times. Consider varying your action verbs')
    elif rating == "Overused":
        alternatives = []
        
        for action_verb in ACTION_VERBS:
            if action_verb != verb:
                alternatives.append(action_verb)
            if len(alternatives) == 3:
                break
                
        alternatives_text = ", ".join(alternatives[: -1]) + f", or {alternatives[-1]}"
        
        report["suggestions"].append(f"{section}: \"{verb}\" is overused. Consider alternatives such as {alternatives_text}")

def count_relevant_numbers(resume_text, number_context_list):
    relevant_number_count = 0
    
    for number_context in number_context_list:
        if not number_context["excluded"]:
            relevant_number_count += 1
    return relevant_number_count
    
def find_number_context(resume_text, excluded_numbers):
    print("Excluded numbers:", excluded_numbers)
    number_matches = re.finditer(r"\d+", resume_text)
    
    number_context_list = []
    
    for match in number_matches:
        start, end = match.start(), match.end()
        
        context_start = max(0, start - 15)
        context_end = min(len(resume_text), end + 15)
        
        context = resume_text[context_start: context_end]

        item = {}
        item["number"] = match.group()
        item["context"] = context
        item["excluded"] = (
            match.group() in excluded_numbers
            or is_education_number(context)
        )
        
        number_context_list.append(item)
        
        print(
            match.group(),
            "Education:", is_education_number(context),
            "Excluded:", item["excluded"]
        )
        
    return number_context_list

def find_excluded_numbers(resume_text):
    year_pattern = r"\b[\d]{4}\b"
    phone_number_pattern = LINK_CHECKS["Phone number"]["pattern"]
    phone_numbers = []
    
    year_list = re.findall(year_pattern, resume_text)
    phone_matches = re.findall(phone_number_pattern, resume_text)
    
    print("Phone regex:", phone_number_pattern)
    print("Phone matches:", phone_matches)
    
    print("Phone context:")
    phone_index = resume_text.find("+91")
    print(resume_text[phone_index:phone_index + 30])
    
    for phone in phone_matches:
        phone_numbers.extend(re.findall(r"\d+", phone))

    return year_list + phone_numbers

def is_education_number(context):
    for keyword in EDUCATION_NUMBER_KEYWORDS:
        if keyword in context:
            return True
        
    for pattern in EDUCATION_PATTERNS:
        if re.search(pattern, context, re.IGNORECASE):
            return True
        
    for pattern in PERCENTAGE_PATTERNS:
        for pattern in EDUCATION_PATTERNS:
            if re.search(pattern, context, re.IGNORECASE):
                return True
        # not checking education keywords as its check is there above already
    return False

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
    
    action_verbs = find_action_verbs(text)  
    
    total_action_verbs = 0
    
    for verb, details in action_verbs.items():
        total_action_verbs += details["frequency"]

    unique_action_verbs = len(action_verbs.keys())
    
    result[f"{lower_key}_action_verbs_frequency"] = action_verbs
    
    all_optimum = True
    for verb, details in action_verbs.items():
        details["rating"] = evaluate_action_verbs_frequency(details["frequency"])
        
        if details["rating"] == "Optimum":
            pass
        else:     
            all_optimum = False
            add_action_verb_freq_feedback(
                details["rating"],
                report,
                verb,
                details["frequency"],
                section
            )
    
    if all_optimum:
        add_action_verb_freq_feedback(
            "Optimum",
            report,
            "",
            "",
            section
        )
        
    result[f"{lower_key}_action_verbs_count"] = total_action_verbs
    result[f"{lower_key}_unique_action_verbs_count"] = unique_action_verbs
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
        
        "action_verbs_frequency": {},
        "action_verbs_count": 0,
        
        "projects_action_verbs_frequency": {},
        "projects_action_verbs_count": 0,
        "experience_action_verbs_count": 0,
        
        "experience_action_verbs_frequency": {},
        "projects_unique_action_verbs_count": 0,
        "experience_unique_action_verbs_count": 0,
        
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
    print("Excluded numbers:", find_excluded_numbers(resume_text))
    resume_lower = resume_text.lower()
    print(find_number_context(resume_text, find_excluded_numbers(resume_text)))
    
    for item in find_number_context(resume_text, find_excluded_numbers(resume_text)):
        print(f"{item["number"]} -> {item["excluded"]}")
    
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
            resume_text,
            report,
            details["report_key"],
            details["pattern"],
            label,
            details["score"]
        )
    
    action_verbs = find_action_verbs(resume_text)
    report["action_verbs_frequency"] = action_verbs
    verb_count = 0
    for verb, details in action_verbs.items():
        verb_count += details["frequency"]
        
    unique_action_verbs = len(action_verbs.keys())
    report["action_verbs_count"] = verb_count
    report["unique_action_verbs"] = unique_action_verbs
    
    if verb_count == 0:
        add_suggestions(report, "Action verbs")
    elif 1 <= verb_count < 4:
        report["strengths"].append(f"Good use of action verbs ({verb_count} detected)")
    elif 4 <= verb_count < 8:
        report["strengths"].append(f"Strong use of action verbs ({verb_count} detected)")
    elif verb_count >= 8:
        report["strengths"].append(f"Excellent use of action verbs ({verb_count} detected)")
    
    excluded_numbers = find_excluded_numbers(resume_text)
    report["numbers_count"] = count_relevant_numbers(resume_text, find_number_context(resume_text, find_excluded_numbers(resume_text)))
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