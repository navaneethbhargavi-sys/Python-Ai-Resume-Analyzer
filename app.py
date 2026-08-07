import streamlit as st
from utils.pdf_reader import extract_text
from utils.ats import analyze_resume

st.set_page_config(
    page_title = "AI Resume Analyzer",
    page_icon = "📄",
    layout = "centered"
)

st.title("📄 AI Resume Analyzer")

st.write(
    "Improve your resume with AI-powered ATS analysis and personalized feedback."
)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type = ["pdf"]
)

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing Resume..."):
            resume_text = extract_text(uploaded_file)
            report = analyze_resume(resume_text)
        
        st.header("📄 AI Resume Analysis")
        st.divider()
        ats_score = report["score"]
        
        def score_color(score, max_score):
            percentage = (score / max_score) * 100
            
            if 80 <= percentage <= 100:
                return "🟢"
            elif 50 <= percentage < 80:
                return "🟡"
            elif 0 <= percentage < 50:
                return "🔴"
        
        ats_score_color = score_color(ats_score, 100)
        st.metric(
            label = "ATS Score",
            value = f"{ats_score_color} {ats_score} / 100"
        )
        st.progress(ats_score)
        st.divider()
        
        left, right = st.columns([4, 1])
        
        for section, details in report["score_breakdown"].items():
            score = details["score"]
            max_score = details["max_score"]
            sc_color = score_color(score, max_score)
            
            left.write(f"{section}")
            right.write(f"{sc_color} {score} / {max_score}")
        st.divider()
        
        left, right = st.columns(2)
        
        # left -> strengths
        left.subheader("Strengths")
        for strength in report["strengths"]:
            left.write(f"✅ {strength}")
        left.write("")
        
        if report["technical_skills_count"] > 0:
            left.markdown(f'**Detected {report["technical_skills_count"]} technical skills**')
            left.write('')
            
            for tech_skill in report["technical_skills"]:
                left.write(f"✅ {tech_skill}")
        
        left.write('')   
        left.markdown("**📊 Resume Statistics**")
        left.write(f"Detected {report["numbers_count"]} numbers in your resume.")
        left.write(f"Word Count: {report["word_count"]}")
        
        # right -> suggestions
        right.subheader("Suggestions")
        for suggestion in report["suggestions"]:
            right.write(f"💡 {suggestion}")
        st.divider()
            
        st.subheader("Missing Sections")
        for missing_section in report["missing_sections"]:
            st.write(f"❌ {missing_section}")
            
        st.write(report["projects_text"])