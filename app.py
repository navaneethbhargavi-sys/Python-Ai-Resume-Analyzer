import streamlit as st

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

st.button("Analyze Resume")