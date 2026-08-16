# """AI-generated assessment page for Talent Sphere Elevate.

# Place this file in the project as: pages/AI_Exam.py

# The page reads the PDFs from the four lesson days before the selected exam day.
# For example, Day 05 reads Documents/Day_01 through Documents/Day_04.
# """

# from __future__ import annotations

# import json
# import re
# from pathlib import Path

# import streamlit as st
# from PyPDF2 import PdfReader
# from src.llm import generate_response


# st.set_page_config(page_title="AI Assessment", page_icon="📝", layout="wide")


# def project_root() -> Path:
#     page_file = Path(__file__).resolve()
#     candidates = (page_file.parent.parent, page_file.parent, Path.cwd())
#     for candidate in candidates:
#         if (candidate / "Documents").exists() or (candidate / "pages").exists():
#             return candidate
#     return page_file.parent.parent


# def selected_exam_day() -> int:
#     """Get the exam day selected from Learning Portal; default to Day 05."""
#     label = st.session_state.get("learning_portal_exam_day", "Day 05")
#     match = re.search(r"\d+", label)
#     return int(match.group()) if match else 5


# def lesson_days_for_exam(exam_day: int) -> range:
#     """Day 05 -> Days 01-04, Day 11 -> Days 07-10, and so on."""
#     return range(exam_day - 4, exam_day)


# def read_pdf(pdf_path: Path) -> str:
#     try:
#         reader = PdfReader(pdf_path)
#         return "\n".join(page.extract_text() or "" for page in reader.pages)
#     except Exception:
#         return ""


# def learning_material_for_exam(exam_day: int) -> tuple[str, list[str]]:
#     material_parts: list[str] = []
#     missing_days: list[str] = []

#     for day in lesson_days_for_exam(exam_day):
#         folder = project_root() / "Documents" / f"Day_{day:02d}"
#         pdf_files = sorted(folder.glob("*.pdf")) if folder.exists() else []

#         if not pdf_files:
#             missing_days.append(f"Day {day:02d}")
#             continue

#         for pdf_file in pdf_files:
#             text = read_pdf(pdf_file)
#             if text.strip():
#                 material_parts.append(f"SOURCE: {pdf_file.name}\n{text}")

#     return "\n\n".join(material_parts), missing_days


# def extract_json(response: str) -> list[dict]:
#     """Read JSON even if the model wraps it in a Markdown code block."""
#     cleaned = response.strip()
#     cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
#     cleaned = re.sub(r"\s*```$", "", cleaned)

#     start = cleaned.find("[")
#     end = cleaned.rfind("]")
#     if start == -1 or end == -1:
#         raise ValueError("The AI did not return a JSON question list.")

#     data = json.loads(cleaned[start : end + 1])
#     if not isinstance(data, list) or len(data) != 10:
#         raise ValueError("The AI must return exactly 10 questions.")

#     questions: list[dict] = []
#     for item in data:
#         question = str(item.get("question", "")).strip()
#         options = item.get("options", [])
#         answer = str(item.get("answer", "")).strip()

#         if not question or not isinstance(options, list) or len(options) != 4:
#             raise ValueError("One generated question is incomplete.")

#         options = [str(option).strip() for option in options]
#         if answer not in options:
#             raise ValueError("One generated answer does not match its options.")

#         questions.append({"question": question, "options": options, "answer": answer})

#     return questions


# def generate_exam_questions(exam_day: int, material: str) -> list[dict]:
#     # Keeps the API request manageable even if PDFs contain many pages.
#     material = material[:30000]

#     prompt = f"""
# You are an assessment creator for an AI learning portal.

# Create a Day {exam_day:02d} assessment using ONLY the learning material below.

# LEARNING MATERIAL:
# {material}

# Requirements:
# - Generate exactly 10 multiple-choice questions.
# - Each question must have exactly 4 options.
# - Include a mix of easy, medium, and application-based questions.
# - Do not ask anything outside the learning material.
# - Do not include explanations, headings, Markdown, or any text outside JSON.
# - The correct answer must exactly match one of the four options.

# Return exactly this valid JSON structure:
# [
#   {{
#     "question": "Question text",
#     "options": ["Option A", "Option B", "Option C", "Option D"],
#     "answer": "Correct option text"
#   }}
# ]
# """

#     return extract_json(generate_response(prompt))


# exam_day = selected_exam_day()
# exam_key = f"ai_exam_questions_day_{exam_day}"
# result_key = f"ai_exam_result_day_{exam_day}"

# st.title(f"📝 Day {exam_day:02d} — AI Assessment")
# st.write(
#     f"This assessment is generated from the PDFs for Days {exam_day - 4:02d} to {exam_day - 1:02d}."
# )
# st.divider()

# material, missing_days = learning_material_for_exam(exam_day)

# if missing_days:
#     st.error("Assessment is locked. Upload PDFs for: " + ", ".join(missing_days))
#     st.stop()

# if not material.strip():
#     st.error("PDF text could not be read. Please use text-based PDFs and try again.")
#     st.stop()

# if exam_key not in st.session_state:
#     with st.spinner("🤖 Creating your AI assessment from the learning PDFs..."):
#         try:
#             st.session_state[exam_key] = generate_exam_questions(exam_day, material)
#         except Exception as error:
#             st.error(f"Could not generate the assessment: {error}")
#             st.stop()

# questions = st.session_state[exam_key]

# if result_key in st.session_state:
#     result = st.session_state[result_key]
#     st.success(f"Your Score: {result['score']}/{len(questions)}")
#     st.info(f"Percentage: {result['percentage']:.0f}%")

#     if result["passed"]:
#         st.success("🎉 Passed! Your mock interview is now unlocked.")
#     else:
#         st.error("You need 70% to pass. Review the PDFs and try again.")

#     if st.button("🔄 Generate a New Assessment", type="primary"):
#         st.session_state.pop(exam_key, None)
#         st.session_state.pop(result_key, None)
#         st.rerun()

#     st.stop()

# answers: dict[int, str] = {}
# for index, question in enumerate(questions, start=1):
#     st.subheader(f"Question {index}")
#     answers[index - 1] = st.radio(
#         question["question"],
#         question["options"],
#         key=f"exam-{exam_day}-{index}",
#     )

# st.divider()

# if st.button("Submit Assessment", type="primary"):
#     score = sum(
#         answers[index] == question["answer"]
#         for index, question in enumerate(questions)
#     )
#     percentage = (score / len(questions)) * 100
#     passed = percentage >= 70

#     st.session_state[result_key] = {
#         "score": score,
#         "percentage": percentage,
#         "passed": passed,
#     }

#     if passed:
#         if "completed_exam_days" not in st.session_state:
#             st.session_state.completed_exam_days = set()
#         st.session_state.completed_exam_days.add(exam_day)

#     st.rerun()


"""Three-section AI assessment page for Talent Sphere Elevate."""

from __future__ import annotations

import json
import re
from pathlib import Path

import streamlit as st
from PyPDF2 import PdfReader

from src.llm import generate_response


st.set_page_config(
    page_title="AI Assessment",
    page_icon="📝",
    layout="wide",
)

PASS_PERCENTAGE = 70
LEARNING_PORTAL_PAGE = "pages/16_Learning_portal.py"


# ---------------------------------------------------------
# PROJECT HELPERS
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


def selected_exam_day() -> int:
    """Read Day 05, Day 11, etc. selected from Learning Portal."""
    selected_day = st.session_state.get("selected_exam_day")

    if isinstance(selected_day, int):
        return selected_day

    old_value = st.session_state.get("learning_portal_exam_day", "Day 05")
    match = re.search(r"\d+", str(old_value))

    return int(match.group()) if match else 5


def lesson_days_for_exam(exam_day: int) -> range:
    """Day 05 uses Days 01-04; Day 11 uses Days 07-10."""
    return range(exam_day - 4, exam_day)


def read_pdf(pdf_path: Path) -> str:
    try:
        reader = PdfReader(pdf_path)

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    except Exception:
        return ""


def learning_material_for_exam(exam_day: int) -> tuple[str, list[str]]:
    material_parts: list[str] = []
    missing_days: list[str] = []

    for lesson_day in lesson_days_for_exam(exam_day):
        folder = project_root() / "Documents" / f"Day_{lesson_day:02d}"
        pdf_files = sorted(folder.glob("*.pdf")) if folder.exists() else []

        if not pdf_files:
            missing_days.append(f"Day {lesson_day:02d}")
            continue

        for pdf_file in pdf_files:
            pdf_text = read_pdf(pdf_file)

            if pdf_text.strip():
                material_parts.append(
                    f"SOURCE: {pdf_file.name}\n{pdf_text}"
                )

    return "\n\n".join(material_parts), missing_days


# ---------------------------------------------------------
# AI QUESTION GENERATION
# ---------------------------------------------------------
def clean_json_response(response: str) -> str:
    cleaned = response.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    return cleaned


def generate_assessment_questions(
    exam_day: int,
    material: str,
) -> dict:
    """Generate 10 MCQs, 5 True/False, and 3 typed questions."""

    material = material[:30000]

    prompt = f"""
You are an assessment creator for an AI learning portal.

Create a Day {exam_day:02d} assessment using ONLY this learning material.

LEARNING MATERIAL:
{material}

Create exactly three sections:

1. mcqs:
- Exactly 10 multiple-choice questions.
- Every question must have exactly 4 options.
- The answer must exactly match one option.

2. true_false:
- Exactly 5 True or False questions.
- The answer must be exactly "True" or "False".

3. short_answers:
- Exactly 3 short-answer questions.
- Students will type answers.
- expected_answer must be a short and accurate model answer.

Rules:
- Use only the supplied learning material.
- Include easy, medium, and application-level questions.
- Return only valid JSON.
- Do not return Markdown or explanations.

Use exactly this format:

{{
  "mcqs": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option text"
    }}
  ],
  "true_false": [
    {{
      "question": "Statement text",
      "answer": "True"
    }}
  ],
  "short_answers": [
    {{
      "question": "Short-answer question",
      "expected_answer": "Short model answer"
    }}
  ]
}}
"""

    response = clean_json_response(generate_response(prompt))

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("AI did not return valid assessment JSON.")

    assessment = json.loads(response[start : end + 1])

    mcqs = assessment.get("mcqs", [])
    true_false = assessment.get("true_false", [])
    short_answers = assessment.get("short_answers", [])

    if len(mcqs) != 10:
        raise ValueError("AI must generate exactly 10 MCQs.")

    if len(true_false) != 5:
        raise ValueError("AI must generate exactly 5 True/False questions.")

    if len(short_answers) != 3:
        raise ValueError("AI must generate exactly 3 short-answer questions.")

    for question in mcqs:
        options = question.get("options", [])

        if (
            not question.get("question")
            or not isinstance(options, list)
            or len(options) != 4
            or question.get("answer") not in options
        ):
            raise ValueError("One MCQ is invalid.")

    for question in true_false:
        if (
            not question.get("question")
            or question.get("answer") not in {"True", "False"}
        ):
            raise ValueError("One True/False question is invalid.")

    for question in short_answers:
        if not question.get("question") or not question.get("expected_answer"):
            raise ValueError("One short-answer question is invalid.")

    return assessment


def grade_short_answers(
    questions: list[dict],
    student_answers: list[str],
) -> list[dict]:
    """Use AI to grade the typed short answers."""

    answers_to_grade = []

    for index, question in enumerate(questions):
        answers_to_grade.append(
            {
                "question_number": index + 1,
                "question": question["question"],
                "expected_answer": question["expected_answer"],
                "student_answer": student_answers[index],
            }
        )

    prompt = f"""
You are grading short answers.

For every answer:
- Give score 1 if the student answer is correct or reasonably correct.
- Give score 0 if it is wrong, unrelated, or blank.
- Give short feedback.

Return ONLY this valid JSON format:

[
  {{
    "question_number": 1,
    "score": 0,
    "feedback": "Short feedback"
  }}
]

DATA:
{json.dumps(answers_to_grade, ensure_ascii=False)}
"""

    response = clean_json_response(generate_response(prompt))

    start = response.find("[")
    end = response.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("AI could not grade the short answers.")

    grades = json.loads(response[start : end + 1])

    if not isinstance(grades, list) or len(grades) != len(questions):
        raise ValueError("Short-answer grading result is incomplete.")

    validated_grades = []

    for index, grade in enumerate(grades):
        score = 1 if int(grade.get("score", 0)) == 1 else 0

        validated_grades.append(
            {
                "question_number": index + 1,
                "score": score,
                "feedback": str(grade.get("feedback", "")).strip(),
            }
        )

    return validated_grades


def clear_exam_state(exam_day: int) -> None:
    """Clear assessment data and old answer widgets."""

    st.session_state.pop(f"ai_exam_questions_day_{exam_day}", None)
    st.session_state.pop(f"ai_exam_result_day_{exam_day}", None)

    for index in range(1, 11):
        st.session_state.pop(f"mcq-{exam_day}-{index}", None)

    for index in range(1, 6):
        st.session_state.pop(f"tf-{exam_day}-{index}", None)

    for index in range(1, 4):
        st.session_state.pop(f"short-{exam_day}-{index}", None)


# ---------------------------------------------------------
# PAGE DESIGN
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .exam-hero {
            padding: 1.6rem 1.9rem;
            border-radius: 18px;
            color: white;
            background: linear-gradient(135deg, #1d4ed8, #7c3aed);
            margin-bottom: 1.2rem;
        }

        .exam-hero h1 {
            margin: 0;
        }

        .exam-hero p {
            margin: 0.4rem 0 0;
            opacity: 0.9;
        }

        .section-title {
            margin-top: 1.5rem;
            margin-bottom: 0.9rem;
            padding: 0.8rem 1rem;
            border-left: 5px solid #4f46e5;
            border-radius: 9px;
            color: #312e81;
            background: #eef2ff;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

exam_day = selected_exam_day()
exam_key = f"ai_exam_questions_day_{exam_day}"
result_key = f"ai_exam_result_day_{exam_day}"

st.markdown(
    f"""
    <div class="exam-hero">
        <h1>📝 Day {exam_day:02d} AI Assessment</h1>
        <p>Complete all sections. Score {PASS_PERCENTAGE}% or above to unlock the AI Mock Interview.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("← Back to Learning Portal"):
    st.switch_page(LEARNING_PORTAL_PAGE)

st.info(
    f"This assessment is generated from PDFs of "
    f"Days {exam_day - 4:02d} to {exam_day - 1:02d}."
)

material, missing_days = learning_material_for_exam(exam_day)

if missing_days:
    st.error(
        "Assessment is locked. Missing PDF material for: "
        + ", ".join(missing_days)
    )
    st.stop()

if not material.strip():
    st.error("PDF text could not be read. Use text-based PDFs.")
    st.stop()


# ---------------------------------------------------------
# CLEAR OLD 10-MCQ DATA AND CREATE NEW THREE-SECTION DATA
# ---------------------------------------------------------
stored_assessment = st.session_state.get(exam_key)

assessment_is_valid = (
    isinstance(stored_assessment, dict)
    and "mcqs" in stored_assessment
    and "true_false" in stored_assessment
    and "short_answers" in stored_assessment
)

if not assessment_is_valid:
    # Deletes your old list-based 10-MCQ exam data automatically.
    st.session_state.pop(exam_key, None)
    st.session_state.pop(result_key, None)

    with st.spinner("🤖 Creating your three-section AI assessment..."):
        try:
            st.session_state[exam_key] = generate_assessment_questions(
                exam_day,
                material,
            )

        except Exception as error:
            st.error(f"Could not generate assessment: {error}")
            st.stop()

assessment = st.session_state[exam_key]
mcqs = assessment["mcqs"]
true_false_questions = assessment["true_false"]
short_answer_questions = assessment["short_answers"]


# ---------------------------------------------------------
# SHOW RESULTS
# ---------------------------------------------------------
stored_result = st.session_state.get(result_key)

result_is_valid = (
    isinstance(stored_result, dict)
    and "score" in stored_result
    and "total_marks" in stored_result
    and "percentage" in stored_result
    and "mcq_score" in stored_result
    and "tf_score" in stored_result
    and "short_score" in stored_result
)

if stored_result and not result_is_valid:
    st.session_state.pop(result_key, None)
    stored_result = None

if stored_result:
    st.success(
        f"Final Score: {stored_result['score']}/{stored_result['total_marks']}"
    )
    st.info(f"Percentage: {stored_result['percentage']:.0f}%")

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:
        st.metric("MCQ Score", f"{stored_result['mcq_score']}/10")

    with score_col2:
        st.metric("True/False Score", f"{stored_result['tf_score']}/5")

    with score_col3:
        st.metric("Short Answer Score", f"{stored_result['short_score']}/3")

    if stored_result["passed"]:
        st.success(
            "🎉 You passed! Your AI Mock Interview is now unlocked."
        )

    else:
        st.error(
            f"You need at least {PASS_PERCENTAGE}% to pass. "
            "Review the PDFs and try again."
        )

    st.markdown(
        '<div class="section-title">Short Answer Feedback</div>',
        unsafe_allow_html=True,
    )

    for grade in stored_result["short_grades"]:
        icon = "✅" if grade["score"] == 1 else "❌"

        st.write(
            f"{icon} Question {grade['question_number']}: "
            f"{grade['feedback']}"
        )

    if st.button("🔄 Generate a New Assessment", type="primary"):
        clear_exam_state(exam_day)
        st.rerun()

    st.stop()


# ---------------------------------------------------------
# SECTION 1: MCQs
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Section 1 · Multiple Choice Questions · 10 Marks</div>',
    unsafe_allow_html=True,
)

mcq_answers: list[str | None] = []

for index, question in enumerate(mcqs, start=1):
    st.write(f"**{index}. {question['question']}**")

    answer = st.radio(
        "Select one option",
        question["options"],
        index=None,
        key=f"mcq-{exam_day}-{index}",
        label_visibility="collapsed",
    )

    mcq_answers.append(answer)
    st.divider()


# ---------------------------------------------------------
# SECTION 2: TRUE / FALSE
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Section 2 · True or False · 5 Marks</div>',
    unsafe_allow_html=True,
)

true_false_answers: list[str | None] = []

for index, question in enumerate(true_false_questions, start=1):
    st.write(f"**{index}. {question['question']}**")

    answer = st.radio(
        "Choose True or False",
        ["True", "False"],
        index=None,
        horizontal=True,
        key=f"tf-{exam_day}-{index}",
        label_visibility="collapsed",
    )

    true_false_answers.append(answer)
    st.divider()


# ---------------------------------------------------------
# SECTION 3: TYPED SHORT ANSWERS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Section 3 · Short Answer Questions · 3 Marks</div>',
    unsafe_allow_html=True,
)

short_answers: list[str] = []

for index, question in enumerate(short_answer_questions, start=1):
    st.write(f"**{index}. {question['question']}**")

    answer = st.text_area(
        "Type your answer",
        height=115,
        placeholder="Write your answer here...",
        key=f"short-{exam_day}-{index}",
        label_visibility="collapsed",
    )

    short_answers.append(answer.strip())
    st.divider()


# ---------------------------------------------------------
# SUBMIT ASSESSMENT
# ---------------------------------------------------------
if st.button(
    "Submit AI Assessment",
    type="primary",
    use_container_width=True,
):
    unanswered_mcqs = [
        index + 1
        for index, answer in enumerate(mcq_answers)
        if answer is None
    ]

    unanswered_tf = [
        index + 1
        for index, answer in enumerate(true_false_answers)
        if answer is None
    ]

    unanswered_short = [
        index + 1
        for index, answer in enumerate(short_answers)
        if not answer
    ]

    if unanswered_mcqs or unanswered_tf or unanswered_short:
        st.warning(
            "Please answer all questions before submitting. "
            f"Missing MCQs: {unanswered_mcqs}; "
            f"True/False: {unanswered_tf}; "
            f"Short Answers: {unanswered_short}"
        )
        st.stop()

    with st.spinner("🤖 AI is evaluating your short answers..."):
        try:
            short_grades = grade_short_answers(
                short_answer_questions,
                short_answers,
            )

        except Exception as error:
            st.error(f"Could not evaluate short answers: {error}")
            st.stop()

    mcq_score = sum(
        answer == question["answer"]
        for answer, question in zip(mcq_answers, mcqs)
    )

    tf_score = sum(
        answer == question["answer"]
        for answer, question in zip(
            true_false_answers,
            true_false_questions,
        )
    )

    short_score = sum(grade["score"] for grade in short_grades)
    total_marks = 18
    final_score = mcq_score + tf_score + short_score
    percentage = (final_score / total_marks) * 100
    passed = percentage >= PASS_PERCENTAGE

    st.session_state[result_key] = {
        "mcq_score": mcq_score,
        "tf_score": tf_score,
        "short_score": short_score,
        "score": final_score,
        "total_marks": total_marks,
        "percentage": percentage,
        "passed": passed,
        "short_grades": short_grades,
    }

    # Unlocks Day 06, Day 12, etc. after passing.
    if passed:
        if "completed_exam_days" not in st.session_state:
            st.session_state.completed_exam_days = set()

        st.session_state.completed_exam_days = set(
            st.session_state.completed_exam_days
        )

        st.session_state.completed_exam_days.add(exam_day)

    st.rerun()