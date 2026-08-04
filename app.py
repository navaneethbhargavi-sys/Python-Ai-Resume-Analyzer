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
        score_color = ""
        
        if 80 <= ats_score <= 100:
            score_color = "🟢"
        elif 50 <= ats_score < 80:
            score_color = "🟡"
        elif 0 <= ats_score < 50:
            score_color = "🔴"
        
        st.metric(
            label = "ATS Score",
            value = f"{score_color} {ats_score} / 100"
        )
        st.progress(ats_score)
        st.divider()
        
        for section, points in report["score_breakdown"].items():
            st.write(f"{section} -> {points}")
        st.divider()
        
        st.subheader("Strengths")
        for strength in report["strengths"]:
            st.write(f"✅ {strength} section found")
        if report["technical_skills_count"] > 0:
            st.write(f'✅ Detected {report["technical_skills_count"]} technical skills')
        st.divider()
        
        st.subheader("Suggestions")
        for weakness in report["weaknesses"]:
            st.write(f"💡 Add a {weakness} section to improve your ATS score.")
        for suggestion in report["suggestions"]:
            st.write(f"Add {suggestion} to your resume to improve your ATS Score")
        st.divider()
            
        st.subheader("Missing Sections")
        for missing_section in report["missing_sections"]:
            st.write(f"❌ {missing_section}")