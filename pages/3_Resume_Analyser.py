import streamlit as st
import PyPDF2
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()


load_dotenv()


st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and get AI-powered feedback."
)


# Initialize AI Model

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


# Upload Resume

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)


if uploaded_file:

    st.success("Resume uploaded successfully ✅")


    # Extract PDF Text

    pdf_reader = PyPDF2.PdfReader(
        uploaded_file
    )

    resume_text = ""

    for page in pdf_reader.pages:
        resume_text += page.extract_text()


    st.subheader("📌 Resume Preview")

    st.text_area(
        "Extracted Text",
        resume_text,
        height=250
    )


    # Resume Analysis Button

    if st.button("🤖 Analyze Resume"):


        with st.spinner("AI is analyzing your resume..."):


            prompt = f"""
            Analyze this resume and provide:

            1. Key technical skills
            2. Strengths
            3. Missing skills
            4. Resume improvement suggestions
            5. ATS friendliness score out of 100

            Resume:
            {resume_text}
            """


            response = llm.invoke(
                [
                    HumanMessage(
                        content=prompt
                    )
                ]
            )


            st.subheader("🤖 AI Feedback")

            st.write(
                response.content
            )