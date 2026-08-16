# import streamlit as st
# from streamlit_mic_recorder import mic_recorder

# st.set_page_config(
#     page_title="AI Mock Interview",
#     page_icon="🎤"
# )

# st.title("🎤 AI Voice Mock Interview")

# st.write(
#     "Question 1: Tell me about yourself"
# )

# audio = mic_recorder(
#     start_prompt="🎙️ Start Recording",
#     stop_prompt="⏹️ Stop Recording",
#     key="voice"
# )

# if audio:
#     st.success("Voice recorded successfully!")

#     st.audio(
#         audio["bytes"],
#         format="audio/wav"
#     )


# import streamlit as st
# from pathlib import Path
# from PyPDF2 import PdfReader
# from src.llm import generate_response
# from gtts import gTTS
# import pygame
# import time
# from streamlit_mic_recorder import speech_to_text
# import tempfile
# import os

# st.set_page_config(
#     page_title="AI Voice Mock Interview",
#     page_icon="🎤",
#     layout="wide"
# )

# st.title("🎤 AI Voice Mock Interview")

# st.markdown("""
# Welcome to **Talent Sphere Elevate AI Interview**.

# The interview will start with a short introduction.

# After that, AI will generate technical interview questions based on your learning PDFs.

# Good Luck!
# """)

# # ------------------------------
# # Voice Function
# # ------------------------------

# def speak(text):

#     try:

#         temp_file = tempfile.NamedTemporaryFile(
#             delete=False,
#             suffix=".mp3"
#         )

#         audio_path = temp_file.name
#         temp_file.close()


#         tts = gTTS(
#             text=text,
#             lang="en"
#         )

#         tts.save(audio_path)


#         pygame.mixer.init()

#         pygame.mixer.music.load(audio_path)

#         pygame.mixer.music.play()


#         while pygame.mixer.music.get_busy():
#             time.sleep(0.2)


#         pygame.mixer.music.stop()

#         pygame.mixer.quit()


#         # small delay to release file
#         time.sleep(1)

#         if os.path.exists(audio_path):
#             os.remove(audio_path)


#     except Exception as e:

#         st.error(f"Voice error: {e}")
# # ------------------------------
# # Read PDFs
# # ------------------------------

# def read_pdf_folder(folder):

#     text = ""

#     folder = Path(folder)

#     if not folder.exists():
#         return ""

#     for pdf in folder.glob("*.pdf"):

#         reader = PdfReader(pdf)

#         for page in reader.pages:

#             page_text = page.extract_text()

#             if page_text:

#                 text += page_text + "\n"

#     return text


# # ------------------------------
# # Read Previous Learning Days
# # ------------------------------

# def get_learning_content():

#     content = ""

#     for day in range(1,5):

#         folder = f"Documents/Day_{day:02d}"

#         content += read_pdf_folder(folder)

#     return content
# # ------------------------------
# # Generate Interview Questions
# # ------------------------------

# def generate_interview():

#     learning_content = get_learning_content()

#     if learning_content.strip() == "":
#         return None

#     prompt = f"""
# You are an experienced AI Technical Interviewer.

# The student has completed Day 01 to Day 04 learning.

# Study the learning material carefully.

# Learning Material:
# {learning_content}

# Interview Flow:

# Start the interview in a friendly and professional manner.

# First greet the student.

# Then ask these questions in the same order:

# 1. Please introduce yourself.
# 2. Tell me about your strengths.
# 3. Why are you interested in learning Python?
# 4. What motivated you to choose AI & Machine Learning?

# After these 4 introductory questions,

# Generate 8 technical interview questions.

# Rules for technical questions:

# - Questions MUST be based ONLY on the learning material provided above.
# - Do NOT ask questions outside the learning material.
# - Ask one question at a time.
# - Questions should be short and interview-like.
# - Do not provide answers.
# - Increase the difficulty gradually.

# Return ONLY in this format:

# WELCOME:
# Welcome to the AI Mock Interview. I hope you are doing well today.

# QUESTIONS:

# Question 1: Please introduce yourself.
# Question 2: Tell me about your strengths.
# Question 3: Why are you interested in learning Python?
# Question 4: What motivated you to choose AI & Machine Learning?
# Question 5: (Generate from Day 01-04 learning material)
# Question 6: (Generate from Day 01-04 learning material)
# Question 7: (Generate from Day 01-04 learning material)
# Question 8: (Generate from Day 01-04 learning material)
# Question 9: (Generate from Day 01-04 learning material)
# Question 10: (Generate from Day 01-04 learning material)
# Question 11: (Generate from Day 01-04 learning material)
# Question 12: (Generate from Day 01-04 learning material)
# """
#     return generate_response(prompt)

# # ------------------------------
# # Session State
# # ------------------------------

# if "started" not in st.session_state:
#     st.session_state.started = False

# if "questions" not in st.session_state:
#     st.session_state.questions = []

# if "current" not in st.session_state:
#     st.session_state.current = 0
# if "answers" not in st.session_state:
#     st.session_state.answers = {}
# if st.sidebar.button("🔄 Reset Interview"):
#     st.session_state.started = False
#     st.session_state.current = 0
#     st.session_state.questions = []
#     st.session_state.answers = {}
#     st.rerun()


# # ------------------------------
# # Start Interview
# # ------------------------------

# if not st.session_state.started:

#     st.info("Click the button below to begin your AI Mock Interview.")

#     if st.button("🎤 Start Interview", type="primary"):

#         interview = generate_interview()

#         if interview is None:

#             st.error("No PDFs found in Day_01 to Day_04.")

#             st.stop()

#         questions = []

#         for line in interview.split("\n"):

#             line = line.strip()

#             if line.startswith("Question"):
#                 questions.append(line)

#         st.session_state.questions = questions
#         st.session_state.started = True
#         st.session_state.current = 0
#         st.session_state.answers = {}

#         st.rerun()
# # ------------------------------
# # Interview Screen
# # ------------------------------

# if st.session_state.started:

#     questions = st.session_state.questions
#     current = st.session_state.current

#     if current < len(questions):

#         st.progress((current + 1) / len(questions))

#         st.subheader("🎤 Interview Question")

#         st.info(questions[current])


#         if st.button("🔊 Listen Question", key=f"listen_{current}"):
#             with st.spinner("AI speaking..."):

#                 speak(questions[current])


#         st.subheader("🎙️ Give your answer")


#         answer = speech_to_text(
#             language="en",
#             start_prompt="🎤 Start Speaking",
#             stop_prompt="⏹️ Stop Speaking",
#             just_once=True,
#             key=f"answer_{current}"
#         )


#         if answer:

#             st.success("Your Answer:")
#             st.write(answer)


#             if "answers" not in st.session_state:
#                 st.session_state.answers = {}


#             st.session_state.answers[current] = answer
#             time.sleep(2)

#             st.session_state.current += 1

#             st.rerun()



#         col1, col2 = st.columns(2)


#         with col1:

#             if st.button("Next Question ➡️", key=f"next_{current}"):

#                 st.session_state.current += 1
#                 st.rerun()



#         with col2:

#             if st.button("Finish Interview", key=f"finish_{current}"):

#                 st.session_state.current = len(questions)
#                 st.rerun()



    
#     else:

#         st.balloons()

#         st.success("🎉 Interview Completed Successfully!")

#         # st.metric("Questions Asked", len(questions))
#         st.metric("Status", "Completed")


#         # ------------------------------
#         # Interview Summary
#         # ------------------------------

#         answers = st.session_state.get("answers", {})

#         total_questions = len(questions)
#         answered_questions = len(answers)

#         st.markdown("## 📋 Interview Summary")

#         st.metric("Total Questions", total_questions)
#         st.metric("Answered Questions", answered_questions)
#         st.metric("Unanswered Questions", total_questions - answered_questions)

#         st.markdown("## 📝 Questions & Your Answers")

#         answers_text = ""

#         for i in range(total_questions):

#             question = questions[i]
#             user_answer = answers.get(i, "Not Answered")

#             st.markdown(f"### Question {i+1}")
#             st.write(question)

#             st.markdown("**Your Answer:**")
#             st.write(user_answer)

#             st.divider()

#             answers_text += f"""
# Question {i+1}
# {question}

# Student Answer:
# {user_answer}

# """

#         # ------------------------------
#         # AI Final Feedback
#         # ------------------------------

#         feedback_prompt = f"""
# You are an experienced AI Technical Interview Evaluator.

# The interview has finished.

# Below are all interview questions and the student's answers.

# {answers_text}

# Generate ONE final interview report.

# Include:

# 1. Overall Performance
# 2. Overall Score (out of 10)
# 3. Technical Knowledge Score (out of 10)
# 4. Communication Skills Score (out of 10)
# 5. Confidence Level
# 6. Strong Points
# 7. Weak Areas
# 8. Suggestions for Improvement
# 9. Final Recommendation

# Evaluate ONLY using the student's answers.
# Do not give generic feedback.
# """

#         with st.spinner("Generating Final AI Feedback..."):

#             feedback = generate_response(feedback_prompt)

#         st.markdown("## 🤖 Final AI Feedback")

#         st.write(feedback)

#         if st.button("🔊 Listen Feedback"):

#             speak(feedback)


import os
import tempfile
import time
from pathlib import Path

import pygame
import streamlit as st
from gtts import gTTS
from PyPDF2 import PdfReader
from streamlit_mic_recorder import speech_to_text

from src.llm import generate_response


st.set_page_config(
    page_title="AI Voice Mock Interview",
    page_icon="🎤",
    layout="wide",
)

LEARNING_PORTAL_PAGE = "pages/16_Learning_portal.py"


# ---------------------------------------------------------
# PROJECT / DAY HELPERS
# ---------------------------------------------------------
def project_root() -> Path:
    page_file = Path(__file__).resolve()

    candidates = (
        page_file.parent.parent,
        page_file.parent,
        Path.cwd(),
    )

    for folder in candidates:
        if (folder / "Documents").exists() or (folder / "pages").exists():
            return folder

    return page_file.parent.parent


def selected_mock_day() -> int:
    """
    Day 06 is the default.
    Learning Portal sends 6, 12, 18, 24, 30, or 36.
    """
    selected_day = st.session_state.get("selected_mock_day", 6)

    if isinstance(selected_day, int):
        return selected_day

    return 6


def learning_days_for_mock(mock_day: int) -> range:
    """
    Day 06 uses Days 01-04.
    Day 12 uses Days 07-10.
    """
    return range(mock_day - 5, mock_day - 1)


def day_label(day_number: int) -> str:
    return f"Day {day_number:02d}"


# ---------------------------------------------------------
# VOICE FUNCTION
# ---------------------------------------------------------
def speak(text: str) -> None:
    audio_path = None

    try:
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3",
        )

        audio_path = temp_file.name
        temp_file.close()

        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.2)

        pygame.mixer.music.stop()
        pygame.mixer.quit()

    except Exception as error:
        st.error(f"Voice error: {error}")

    finally:
        time.sleep(0.5)

        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except OSError:
                pass


# ---------------------------------------------------------
# PDF FUNCTIONS
# ---------------------------------------------------------
def read_pdf_folder(folder: Path) -> str:
    content = ""

    if not folder.exists():
        return content

    for pdf_file in folder.glob("*.pdf"):
        try:
            reader = PdfReader(pdf_file)

            for page in reader.pages:
                page_text = page.extract_text() or ""
                content += page_text + "\n"

        except Exception:
            continue

    return content


def get_learning_content(mock_day: int) -> str:
    content = ""

    for lesson_day in learning_days_for_mock(mock_day):
        folder = project_root() / "Documents" / f"Day_{lesson_day:02d}"
        content += read_pdf_folder(folder)

    return content


# ---------------------------------------------------------
# AI INTERVIEW GENERATION
# ---------------------------------------------------------
def generate_interview(mock_day: int) -> list[str]:
    learning_content = get_learning_content(mock_day)

    if not learning_content.strip():
        return []

    first_lesson_day = mock_day - 5
    last_lesson_day = mock_day - 2

    prompt = f"""
You are an experienced AI Technical Interviewer.

The student has completed learning material from
Day {first_lesson_day:02d} to Day {last_lesson_day:02d}.

LEARNING MATERIAL:
{learning_content[:30000]}

Create exactly 12 interview questions.

Questions 1 to 4 must be exactly:

Question 1: Please introduce yourself.
Question 2: Tell me about your strengths.
Question 3: Why are you interested in this domain?
Question 4: What motivated you to choose AI and Machine Learning?

Questions 5 to 12:
- Generate 8 technical questions.
- Use ONLY the learning material above.
- Keep questions short and professional.
- Do not provide answers.

Return ONLY these twelve lines:

Question 1: ...
Question 2: ...
Question 3: ...
...
Question 12: ...
"""

    response = generate_response(prompt)
    questions = []

    for line in response.splitlines():
        line = line.strip()

        if line.lower().startswith("question"):
            questions.append(line)

    return questions[:12]


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
mock_day = selected_mock_day()

started_key = f"mock_started_day_{mock_day}"
questions_key = f"mock_questions_day_{mock_day}"
current_key = f"mock_current_day_{mock_day}"
answers_key = f"mock_answers_day_{mock_day}"
feedback_key = f"mock_feedback_day_{mock_day}"
completed_key = f"mock_completed_day_{mock_day}"

if started_key not in st.session_state:
    st.session_state[started_key] = False

if questions_key not in st.session_state:
    st.session_state[questions_key] = []

if current_key not in st.session_state:
    st.session_state[current_key] = 0

if answers_key not in st.session_state:
    st.session_state[answers_key] = {}

if "completed_mock_days" not in st.session_state:
    st.session_state.completed_mock_days = set()

st.session_state.completed_mock_days = set(
    st.session_state.completed_mock_days
)


# ---------------------------------------------------------
# PAGE DESIGN
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .interview-hero {
            padding: 1.6rem 1.9rem;
            border-radius: 18px;
            color: white;
            background: linear-gradient(135deg, #0f766e, #2563eb);
            margin-bottom: 1.2rem;
        }

        .interview-hero h1 {
            margin: 0;
        }

        .interview-hero p {
            margin: 0.4rem 0 0;
            opacity: 0.9;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="interview-hero">
        <h1>🎤 {day_label(mock_day)} AI Voice Mock Interview</h1>
        <p>Answer using your voice. Complete the interview to unlock the next learning cycle.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("← Back to Learning Portal"):
    st.switch_page(LEARNING_PORTAL_PAGE)

st.info(
    f"Technical questions are generated from "
    f"Days {mock_day - 5:02d} to {mock_day - 2:02d} learning PDFs."
)


# ---------------------------------------------------------
# RESET INTERVIEW
# ---------------------------------------------------------
if st.sidebar.button("🔄 Reset This Interview"):
    st.session_state[started_key] = False
    st.session_state[questions_key] = []
    st.session_state[current_key] = 0
    st.session_state[answers_key] = {}
    st.session_state.pop(feedback_key, None)
    st.session_state.pop(completed_key, None)

    st.session_state.completed_mock_days.discard(mock_day)
    st.rerun()


# ---------------------------------------------------------
# START INTERVIEW
# ---------------------------------------------------------
if not st.session_state[started_key]:
    st.subheader("Ready to begin?")
    st.write(
        "The interview contains four introductory questions "
        "and eight technical questions."
    )

    if st.button("🎤 Start Interview", type="primary"):
        with st.spinner("🤖 Preparing your AI interview questions..."):
            questions = generate_interview(mock_day)

        if len(questions) < 12:
            st.error(
                "Could not create all interview questions. "
                "Please check that the learning PDFs contain readable text."
            )
            st.stop()

        st.session_state[questions_key] = questions
        st.session_state[current_key] = 0
        st.session_state[answers_key] = {}
        st.session_state[started_key] = True
        st.session_state.pop(feedback_key, None)
        st.session_state.pop(completed_key, None)

        st.rerun()

    st.stop()


# ---------------------------------------------------------
# INTERVIEW QUESTIONS
# ---------------------------------------------------------
questions = st.session_state[questions_key]
current_question = st.session_state[current_key]
answers = st.session_state[answers_key]

if current_question < len(questions):
    st.progress((current_question + 1) / len(questions))
    st.caption(
        f"Question {current_question + 1} of {len(questions)}"
    )

    st.subheader("🎤 Interview Question")
    st.info(questions[current_question])

    if st.button(
        "🔊 Listen to Question",
        key=f"listen_{mock_day}_{current_question}",
    ):
        with st.spinner("AI is speaking..."):
            speak(questions[current_question])

    st.subheader("🎙️ Give Your Answer")

    answer = speech_to_text(
        language="en",
        start_prompt="🎤 Start Speaking",
        stop_prompt="⏹️ Stop Speaking",
        just_once=True,
        key=f"answer_{mock_day}_{current_question}",
    )

    if answer:
        st.success("Your Answer")
        st.write(answer)

        st.session_state[answers_key][current_question] = answer
        st.session_state[current_key] += 1
        st.rerun()

    next_col, finish_col = st.columns(2)

    with next_col:
        if st.button(
            "Next Question ➡️",
            key=f"next_{mock_day}_{current_question}",
            use_container_width=True,
        ):
            st.session_state[current_key] += 1
            st.rerun()

    with finish_col:
        if st.button(
            "Finish Interview",
            key=f"finish_{mock_day}_{current_question}",
            use_container_width=True,
        ):
            st.session_state[current_key] = len(questions)
            st.rerun()

    st.stop()


# ---------------------------------------------------------
# INTERVIEW COMPLETED: UNLOCK NEXT LESSON DAY
# ---------------------------------------------------------
if completed_key not in st.session_state:
    # This is the important code that unlocks Day 07 after Day 06.
    st.session_state.completed_mock_days.add(mock_day)
    st.session_state[completed_key] = True

st.balloons()
st.success("🎉 Interview Completed Successfully!")
st.success(
    f"✅ {day_label(mock_day + 1)} is now unlocked in the Learning Portal."
)

st.metric("Status", "Completed")

total_questions = len(questions)
answered_questions = len(answers)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric("Questions Asked", total_questions)

with summary_col2:
    st.metric("Answers Given", answered_questions)

with summary_col3:
    st.metric("Unanswered", total_questions - answered_questions)

st.markdown("## 📋 Interview Summary")

answers_text = ""

for index in range(total_questions):
    question = questions[index]
    user_answer = answers.get(index, "Not Answered")

    with st.expander(f"Question {index + 1}", expanded=False):
        st.write(question)
        st.markdown("**Your Answer:**")
        st.write(user_answer)

    answers_text += f"""
Question {index + 1}:
{question}

Student Answer:
{user_answer}

"""


# ---------------------------------------------------------
# FINAL AI FEEDBACK
# ---------------------------------------------------------
if feedback_key not in st.session_state:
    feedback_prompt = f"""
You are an experienced AI Technical Interview Evaluator.

Evaluate this completed interview using only the student's answers.

INTERVIEW DATA:
{answers_text}

Create a professional report with:

1. Overall Performance
2. Overall Score out of 10
3. Technical Knowledge Score out of 10
4. Communication Skills Score out of 10
5. Confidence Level
6. Strong Points
7. Areas for Improvement
8. Suggestions for Improvement
9. Final Recommendation
"""

    with st.spinner("🤖 Generating Final AI Feedback..."):
        st.session_state[feedback_key] = generate_response(feedback_prompt)

feedback = st.session_state[feedback_key]

st.markdown("## 🤖 Final AI Feedback")
st.write(feedback)

if st.button("🔊 Listen to Feedback"):
    with st.spinner("AI is speaking..."):
        speak(feedback)

if st.button(
    "Continue to Learning Portal",
    type="primary",
    use_container_width=True,
):
    st.switch_page(LEARNING_PORTAL_PAGE)