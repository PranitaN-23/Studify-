import streamlit as st
import google.generativeai as genai
import os
from utils.read_pdf import read_pdf

genai.configure(api_key=st.secrets.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-pro")

st.set_page_config(
    page_title="Smart Notes Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📚 Studify")
st.caption("Summarize your notes, create flashcards, generate quizzes, or ask questions!")

tabs = st.tabs(["💬 Ask a Question","📘 Notes Assistant" ])

with tabs[0]:
    st.subheader("💬 Ask a Question or Topic")

    question = st.text_area("Enter your question or topic:")
    level = st.radio("Select explanation level:", ["Basic", "Detailed"], horizontal=True)

    if st.button("🔍 Explain"):
        if not question.strip():
            st.warning("Please enter a question or topic.")
        else:
            
            prompt = f"Explain the following topic in a {level.lower()} way:\n\n{question}"
            
            with st.status("⏳ Generating...", expanded=False) as status:
                try:
                    response = model.generate_content(prompt)
                    status.update(label="✅ Done!", state="complete",   expanded=False)
                    st.markdown(response.text)
        
                except Exception as e:
                    status.update(label="❌ Error   occurred", state="error",  expanded=False)
                    st.error(f"{e}")

with tabs[1]:
    mode = st.radio("Select Mode:", ["📘 Summarize Notes", "🧠 Flashcards", "📝 Quiz Generator"])

    upload_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    text_input = st.text_area("Paste your notes here:")

    if st.button("✨ Generate"):
        if not upload_file and not text_input.strip():
            st.warning("Please upload file or paste your notes.")
        else:
            text = read_pdf(upload_file) if upload_file else text_input
            
            if mode == "📘 Summarize Notes":
                prompt = f"Summarize the following notes clearly and concisely:\n\n{text}"

            elif mode == "🧠 Flashcards":
                prompt = f"Create 10 helpful Q&A flashcards from these notes:\n\n{text}"

            elif mode == "📝 Quiz Generator":
                prompt = f"Generate 10 multiple-choice questions with options and correct answers from these notes:\n\n{text}"

            with st.status("⏳ Generating...", expanded=False) as status:
                try:
                    response = model.generate_content(prompt)
                    status.update(label="✅ Done!", state="complete",   expanded=False)
                    st.markdown(response.text)
        
                except Exception as e:
                    status.update(label="❌ Error   occurred", state="error",  expanded=False)
                    st.error(f"{e}")
