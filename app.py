import streamlit as st
from utils.pdf_reader import extract_text
from utils.ats import analyze_resume
import time

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
        
        st.write(report)