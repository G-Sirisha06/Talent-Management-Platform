# import streamlit as st
# from dotenv import load_dotenv
# import os

# from langchain_groq import ChatGroq
# from langchain_core.messages import HumanMessage
# from src.sidebar import hide_Pages_sidebar
# hide_Pages_sidebar()

# # Load environment variables
# load_dotenv()


# # Page Configuration
# st.set_page_config(
#     page_title="AI Chatbot",
#     page_icon="🤖",
#     layout="wide"
# )


# # Title
# st.title("🤖 AI Career Assistant")

# st.write(
#     "Ask questions related to coding, AI, ML, interviews and career guidance."
# )


# # Initialize AI Model

# try:

#     llm = ChatGroq(
#         model="llama-3.1-8b-instant",
#         api_key=os.getenv("GROQ_API_KEY")
#     )

# except Exception as e:

#     st.error(
#         f"API Configuration Error: {e}"
#     )


# # Chat History

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []


# # Display Previous Messages

# for chat in st.session_state.chat_history:

#     with st.chat_message(chat["role"]):
#         st.write(chat["message"])



# # User Input

# question = st.chat_input(
#     "Ask your question..."
# )


# if question:

#     # Show User Message

#     st.chat_message("user").write(
#         question
#     )


#     st.session_state.chat_history.append(
#         {
#             "role": "user",
#             "message": question
#         }
#     )


#     # Get AI Response

#     try:

#         response = llm.invoke(
#             [
#                 HumanMessage(
#                     content=question
#                 )
#             ]
#         )


#         answer = response.content


#         # Show AI Response

#         st.chat_message("assistant").write(
#             answer
#         )


#         st.session_state.chat_history.append(
#             {
#                 "role": "assistant",
#                 "message": answer
#             }
#         )


#     except Exception as e:

#         st.error(
#             f"Something went wrong: {e}"
#         )


import streamlit as st
import time
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import tempfile
import os
import sqlite3
import json
from src.llm import generate_response
from src.rag import retrieve
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()
def save_exam_to_database(title, questions_json):

    conn = sqlite3.connect("talent_sphere.db")
    cursor = conn.cursor()

    # Save Exam
    cursor.execute(
        """
        INSERT INTO exams(exam_name)
        VALUES(?)
        """,
        (title,)
    )

    exam_id = cursor.lastrowid


    # Convert JSON
    questions = json.loads(questions_json)


    # Save Questions
    for q in questions:

        cursor.execute(
            """
            INSERT INTO questions
            (
            exam_id,
            question,
            option1,
            option2,
            option3,
            option4,
            answer
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                exam_id,
                q["question"],
                q["option1"],
                q["option2"],
                q["option3"],
                q["option4"],
                q["answer"]
            )
        )


    conn.commit()
    conn.close()
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Chatbot")
st.caption("Powered by Groq + RAG")

# -----------------------
# Chat History
# -----------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
    
    if "exam_mode" not in st.session_state:
        st.session_state.exam_mode = False
    if "exam_step" not in st.session_state:
        st.session_state.exam_step = 0
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
    
# -----------------------
# Sidebar
# -----------------------

with st.sidebar:

    st.header("⚙️ Settings")

    k = st.slider(
        "Top Results",
        1,
        10,
        5
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.3
    )

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------
# Uploads
# -----------------------

c1, c2 = st.columns(2)

with c1:
    pdf = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

with c2:
    image = st.file_uploader(
        "🖼 Upload Image",
        type=["png","jpg","jpeg"]
    )

# -----------------------
# Suggested Questions
# -----------------------

st.subheader("💡 Suggested Questions")

col1,col2,col3 = st.columns(3)

with col1:

    if st.button("📄 Summarize Document"):
        st.session_state.prompt = "Summarize the uploaded document."

    if st.button("📝 Generate Notes"):
        st.session_state.prompt = "Generate notes."

with col2:

    if st.button("🎯 Interview Questions"):
        st.session_state.prompt = "Generate interview questions."

    if st.button("💼 Resume Feedback"):
        st.session_state.prompt = "Review my resume."

with col3:

    if st.button("📚 Explain Topic"):
        st.session_state.prompt = "Explain this topic."

    if st.button("🚀 Career Guidance"):
        st.session_state.prompt = "Give career guidance."

st.divider()

# -----------------------
# Display Chat
# -----------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

default_prompt = st.session_state.get("prompt", "")
st.subheader("🎤 Voice Assistant")

voice_text = speech_to_text(
    language="en",
    use_container_width=True,
    just_once=True,
    key="voice"
)

if voice_text:
    st.success(f"You said: {voice_text}")

typed_prompt = st.chat_input(
    "Ask anything...",
    key="chatbox"
)

prompt = voice_text if voice_text else typed_prompt

if default_prompt and not prompt:
    prompt = default_prompt
    st.session_state.prompt = ""

if prompt:
    # =====================================
# AI Exam Creation Assistant
# =====================================

    if not st.session_state.exam_mode and prompt.lower() == "create exam":

        st.session_state.exam_mode = True
        st.session_state.exam_step = 1
        st.session_state.exam_data = {}

        st.chat_message("assistant").write(
            "📝 Step 1/7\n\nEnter the Exam Title."
        )

        st.stop()


    if st.session_state.exam_mode:

        # STEP 1
        if st.session_state.exam_step == 1:

            st.session_state.exam_data["title"] = prompt
            st.session_state.exam_step = 2

            st.chat_message("assistant").write(
                "✅ Title Saved.\n\n📚 Step \n\nEnter the Subject."
            )

            st.stop()

        # STEP 2
        elif st.session_state.exam_step == 2:

            st.session_state.exam_data["subject"] = prompt
            st.session_state.exam_step = 3

            st.chat_message("assistant").write(
                "✅ Subject Saved.\n\n❓ Step \n\nHow many questions should I generate?"
            )

            st.stop()

        # STEP 3
        elif st.session_state.exam_step == 3:

            st.session_state.exam_data["questions"] = prompt
            st.session_state.exam_step = 4

            st.chat_message("assistant").write(
                "✅ Number of Questions Saved.\n\n🏆 Step \n\nEnter Total Marks."
            )

            st.stop()

        # STEP 4
        elif st.session_state.exam_step == 4:

            st.session_state.exam_data["marks"] = prompt
            st.session_state.exam_step = 5

            st.chat_message("assistant").write(
                "✅ Marks Saved.\n\n⏰ Step \n\nEnter Time Limit (Minutes)."
            )

            st.stop()

        # STEP 5
        elif st.session_state.exam_step == 5:

            st.session_state.exam_data["time"] = prompt
            st.session_state.exam_step = 6

            st.chat_message("assistant").write(
                "✅ Time Saved.\n\n🎯 Step \n\nDifficulty? (Easy / Medium / Hard)"
            )

            st.stop()

        # STEP 6
        elif st.session_state.exam_step == 6:

            st.session_state.exam_data["difficulty"] = prompt
            st.session_state.exam_step = 7

            st.chat_message("assistant").write(
                "✅ Difficulty Saved.\n\n📋 Step \n\nEnter Exam Instructions."
            )

            st.stop()
        # STEP 7
        elif st.session_state.exam_step == 7:

            st.session_state.exam_data["instructions"] = prompt

            title = st.session_state.exam_data["title"]
            subject = st.session_state.exam_data["subject"]
            num_questions = st.session_state.exam_data["questions"]
            marks = st.session_state.exam_data["marks"]
            time_limit = st.session_state.exam_data["time"]
            difficulty = st.session_state.exam_data["difficulty"]
            instructions = st.session_state.exam_data["instructions"]

            ai_prompt = f"""
            Generate exactly {num_questions} multiple choice questions.

            Exam Title: {title}
            Subject: {subject}
            Difficulty: {difficulty}
            Total Marks: {marks}
            Time Limit: {time_limit} minutes

            Instructions:
            {instructions}

            Return ONLY JSON.

            Example:

            [
            {{
                "question": "What is Python?",
                "option1": "Programming Language",
                "option2": "Database",
                "option3": "Browser",
                "option4": "Operating System",
                "answer": "option1"
            }}
            ]

            Rules:
            - Return only JSON.
            - Do not use markdown.
            - Do not add explanations.
            - Generate exactly {num_questions} questions.
            """

            answer = generate_response(ai_prompt)


            try:

                save_exam_to_database(
                    title,
                    answer
                )

                st.chat_message("assistant").markdown(answer)

                st.success(
                    "🎉 Exam created successfully and saved to database."
                )

            except Exception as e:

                st.error(e)
            st.session_state.exam_mode = False
            st.session_state.exam_step = 0
            st.session_state.exam_data = {}

            st.stop()
    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        context, sources = retrieve(prompt, k)

        full_prompt = f"""
        You are Talent Sphere AI Assistant.

        Instructions:
        - If the provided context is useful, use it naturally in your answer.
        - If the context is not useful, answer normally using your own knowledge.
        - Never say "The uploaded documents do not contain..."
        - Never mention whether you used uploaded documents or not.
        - Give a direct, natural answer.

        Context:
        {context}

        Question:
        {prompt}
        """

        answer = generate_response(full_prompt)
        tts = gTTS(text=answer, lang="en")

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        st.audio(temp_file.name)
        full_response = ""

        for word in answer.split():
            full_response += word + " "
            placeholder.markdown(full_response + "▌")
            time.sleep(0.02)

        placeholder.markdown(full_response)
        if len(sources) > 0:

            st.markdown("### 📚 Sources")

            for s in sources:
                st.write(f"📄 {s['source']} (Page {s['page']})")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    