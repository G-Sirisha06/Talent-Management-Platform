
# """Talent Sphere Elevate - Learning Portal.

# Place this file in your project as: pages/Learning_Portal.py

# Lesson PDFs are loaded from Documents/Day_XX.  For example:
# Documents/Day_01/Python_Introduction.pdf
# """

# from __future__ import annotations

# from pathlib import Path

# import streamlit as st


# st.set_page_config(page_title="Learning Portal", page_icon="📚", layout="wide")


# EXAM_DAYS = {5, 11, 17, 23, 29, 35}
# MOCK_INTERVIEW_DAYS = {6, 12, 18, 24, 30, 36}


# def day_label(day_number: int) -> str:
#     return f"Day {day_number:02d}"


# def project_root() -> Path:
#     """Find the folder that contains the pages and Documents folders."""
#     page_file = Path(__file__).resolve()
#     candidates = (page_file.parent.parent, page_file.parent, Path.cwd())

#     for candidate in candidates:
#         if (candidate / "Documents").exists() or (candidate / "pages").exists():
#             return candidate

#     return page_file.parent.parent


# def pdf_files_for(day_number: int) -> list[Path]:
#     folder = project_root() / "Documents" / f"Day_{day_number:02d}"
#     if not folder.exists():
#         return []

#     return sorted(
#         (
#             file
#             for file in folder.iterdir()
#             if file.is_file() and file.suffix.lower() == ".pdf"
#         ),
#         key=lambda file: file.name.lower(),
#     )


# def required_lesson_days(activity_day: int) -> range:
#     """Return the four lesson days in this six-day learning cycle."""
#     # Exam: Day 05 uses Days 01-04. Mock interview: Day 06 also uses Days 01-04.
#     # The same pattern repeats for Days 11/12, 17/18, and so on.
#     if activity_day in MOCK_INTERVIEW_DAYS:
#         return range(activity_day - 5, activity_day - 1)
#     return range(activity_day - 4, activity_day)


# def activity_is_ready(activity_day: int) -> bool:
#     """Check the correct unlock rule for an assessment or mock interview."""
#     lessons_ready = all(
#         pdf_files_for(day_number) for day_number in required_lesson_days(activity_day)
#     )

#     if activity_day in MOCK_INTERVIEW_DAYS:
#         required_exam_day = activity_day - 1
#         completed_exams = st.session_state.get("completed_exam_days", set())
#         return lessons_ready and required_exam_day in completed_exams

#     return lessons_ready


# def missing_lesson_days(activity_day: int) -> list[str]:
#     """Give a clear message showing which lesson PDFs still need to be uploaded."""
#     return [
#         day_label(day_number)
#         for day_number in required_lesson_days(activity_day)
#         if not pdf_files_for(day_number)
#     ]


# def locked_activity_message(activity_day: int) -> str:
#     """Explain exactly why a particular exam or interview is still locked."""
#     missing_days = missing_lesson_days(activity_day)
#     if missing_days:
#         return f"Upload PDFs for: {', '.join(missing_days)}."

#     if activity_day in MOCK_INTERVIEW_DAYS:
#         return f"Complete the Day {activity_day - 1:02d} AI assessment first."

#     return "This activity is not available yet."


# def page_exists(filename: str) -> bool:
#     return (project_root() / "pages" / filename).exists()


# def open_related_page(filename: str, unavailable_message: str) -> None:
#     if page_exists(filename):
#         st.switch_page(f"pages/{filename}")
#     else:
#         st.error(unavailable_message)


# def open_lesson(day_number: int) -> None:
#     """Open the first PDF for the selected lesson directly in the portal."""
#     pdf_files = pdf_files_for(day_number)
#     if not pdf_files:
#         st.session_state["learning_portal_message"] = f"No PDF found for {day_label(day_number)}."
#         st.session_state.pop("viewing_pdf", None)
#         return

#     st.session_state["viewing_pdf"] = str(pdf_files[0])
#     st.session_state["viewing_lesson_day"] = day_number
#     st.session_state.pop("learning_portal_message", None)


# def show_pdf_viewer() -> None:
#     """Render the selected lesson PDF without a second day-selection step."""
#     message = st.session_state.get("learning_portal_message")
#     if message:
#         st.warning(message)

#     selected_path = st.session_state.get("viewing_pdf")
#     if not selected_path:
#         return

#     pdf_path = Path(selected_path)
#     if not pdf_path.exists():
#         st.session_state.pop("viewing_pdf", None)
#         st.warning("The selected PDF is no longer available.")
#         return

#     lesson_day = st.session_state.get("viewing_lesson_day")
#     heading = day_label(lesson_day) if lesson_day else pdf_path.stem.replace("_", " ")
#     st.markdown(f"## 📖 {heading}")

#     top_left, top_right = st.columns([1, 5])
#     with top_left:
#         if st.button("✕ Close PDF", key="close-pdf"):
#             st.session_state.pop("viewing_pdf", None)
#             st.session_state.pop("viewing_lesson_day", None)
#             st.rerun()
#     with top_right:
#         st.download_button(
#             "⬇️ Download PDF",
#             data=pdf_path.read_bytes(),
#             file_name=pdf_path.name,
#             mime="application/pdf",
#             key=f"download-{pdf_path.name}",
#         )

#     if lesson_day:
#         if lesson_day in st.session_state.completed_learning_days:
#             st.success(f"✅ {day_label(lesson_day)} is marked as completed.")
#         elif st.button(
#             "✅ Mark as Completed",
#             key=f"mark-complete-{lesson_day}",
#             type="primary",
#         ):
#             st.session_state.completed_learning_days.add(lesson_day)
#             st.rerun()

#     try:
#         st.pdf(pdf_path, height=760, key=f"pdf-{pdf_path.name}")
#     except (AttributeError, ImportError, ModuleNotFoundError):
#         st.info("PDF preview is unavailable in this Streamlit version. Use Download PDF to open it.")

#     st.divider()


# if "completed_learning_days" not in st.session_state:
#     st.session_state.completed_learning_days = set()
# if "completed_exam_days" not in st.session_state:
#     st.session_state.completed_exam_days = set()


# st.markdown(
#     """
#     <style>
#     .block-container {max-width: 1250px; padding-top: 2rem; padding-bottom: 3rem;}
#     .portal-hero {
#         background: linear-gradient(110deg, #15803d, #22c55e);
#         color: white; border-radius: 18px; padding: 28px 32px; margin-bottom: 1.25rem;
#         box-shadow: 0 8px 24px rgba(21, 128, 61, .18);
#     }
#     .portal-hero h1 {margin: 0; font-size: 2.15rem;}
#     .portal-hero p {margin: .45rem 0 0; font-size: 1.05rem; opacity: .96;}
#     .stat-card {
#         background: #fff; border: 1px solid #e5e7eb; border-radius: 14px;
#         padding: 16px; text-align: center; box-shadow: 0 2px 10px rgba(15, 23, 42, .06);
#     }
#     .stat-card .number {font-size: 1.7rem; font-weight: 750; color: #166534;}
#     .stat-card .caption {color: #64748b; font-size: .9rem; margin-top: 3px;}
#     .week-heading {color: #166534; margin: 1.5rem 0 .35rem;}
#     div[data-testid="stButton"] > button {
#         min-height: 70px; border-radius: 12px; border: 1px solid #dbe4dc;
#         background: #ffffff; color: #1f2937; font-weight: 650;
#         transition: all .15s ease;
#     }
#     div[data-testid="stButton"] > button:hover {
#         border-color: #22c55e; color: #166534; background: #f0fdf4;
#         transform: translateY(-1px); box-shadow: 0 5px 14px rgba(22, 101, 52, .12);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.markdown(
#     """
#     <div class="portal-hero">
#       <h1>📚 Learning Portal</h1>
#       <p>Choose a day to open its lesson, assessment, or mock interview.</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# completed_count = len(st.session_state.completed_learning_days)
# stat_values = (
#     ("36", "Total Days"),
#     (str(completed_count), "Completed"),
#     ("6", "Assessments"),
#     ("6", "Mock Interviews"),
# )

# for column, (number, caption) in zip(st.columns(4), stat_values):
#     with column:
#         st.markdown(
#             f'<div class="stat-card"><div class="number">{number}</div>'
#             f'<div class="caption">{caption}</div></div>',
#             unsafe_allow_html=True,
#         )

# st.markdown("#### 📈 Your learning progress")
# st.progress(completed_count / 36, text=f"{completed_count} of 36 days completed")

# # A lesson card shows its PDF immediately on this page.  Assessment and mock
# # interview cards navigate immediately to their respective pages.
# show_pdf_viewer()

# st.markdown("### 📅 Course roadmap")
# st.caption("📘 Lesson &nbsp;&nbsp; 📝 Assessment &nbsp;&nbsp; 🎤 Mock interview")

# for week_number in range(1, 7):
#     first_day = (week_number - 1) * 6 + 1
#     st.markdown(f'<h3 class="week-heading">Week {week_number}</h3>', unsafe_allow_html=True)

#     for day_number, column in zip(range(first_day, first_day + 6), st.columns(6)):
#         if day_number in EXAM_DAYS:
#             icon = "📝" if activity_is_ready(day_number) else "🔒"
#         elif day_number in MOCK_INTERVIEW_DAYS:
#             icon = "🎤" if activity_is_ready(day_number) else "🔒"
#         else:
#             icon = "📘"

#         completed_mark = " ✅" if day_number in st.session_state.completed_learning_days else ""

#         with column:
#             if st.button(
#                 f"{icon} {day_label(day_number)}{completed_mark}",
#                 key=f"day-card-{day_number}",
#                 use_container_width=True,
#             ):
#                 if day_number in EXAM_DAYS:
#                     if activity_is_ready(day_number):
#                         st.session_state["learning_portal_exam_day"] = day_label(day_number)
#                         open_related_page(
#                             "AI_Exam.py",
#                             "AI assessment page not found. Create pages/AI_Exam.py first.",
#                         )
#                     else:
#                         st.warning(
#                             f"{day_label(day_number)} is locked. {locked_activity_message(day_number)}"
#                         )
#                 elif day_number in MOCK_INTERVIEW_DAYS:
#                     if activity_is_ready(day_number):
#                         st.session_state["learning_portal_interview_day"] = day_label(day_number)
#                         open_related_page(
#                             "17_Voice_Mock_Interview.py",
#                             "Voice mock interview page not found. Create pages/17_Voice_Mock_Interview.py first.",
#                         )
#                     else:
#                         st.warning(
#                             f"{day_label(day_number)} is locked. {locked_activity_message(day_number)}"
#                         )
#                 else:
#                     open_lesson(day_number)

# st.divider()
# st.caption("Lessons open their PDF directly. Assessment and mock-interview days open their respective pages directly.")


"""Talent Sphere Elevate - Professional Learning Portal."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()


st.set_page_config(
    page_title="Learning Portal",
    page_icon="📚",
    layout="wide",
)

TOTAL_DAYS = 36
EXAM_DAYS = {5, 11, 17, 23, 29, 35}
MOCK_INTERVIEW_DAYS = {6, 12, 18, 24, 30, 36}


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def project_root() -> Path:
    """Find the main project folder."""
    page_file = Path(__file__).resolve()

    candidates = (
        page_file.parent.parent,
        page_file.parent,
        Path.cwd(),
    )

    for folder in candidates:
        if (folder / "pages").exists() or (folder / "Documents").exists():
            return folder

    return page_file.parent.parent


def day_label(day_number: int) -> str:
    return f"Day {day_number:02d}"


def required_lessons_for_exam(exam_day: int) -> range:
    """Example: Day 05 assessment needs Days 01-04."""
    return range(exam_day - 4, exam_day)


def find_activity_page(activity: str) -> str | None:
    """Find the user Exam or Mock Interview Streamlit page."""
    pages_folder = project_root() / "pages"

    if not pages_folder.exists():
        return None

    for page_file in pages_folder.glob("*.py"):
        filename = page_file.name.lower()

        # Do not navigate to an admin page.
        if "admin" in filename:
            continue

        if activity == "exam":
            if "exam" in filename or "assessment" in filename:
                return str(page_file.relative_to(project_root())).replace("\\", "/")

        if activity == "mock":
            if "mock" in filename or "interview" in filename:
                return str(page_file.relative_to(project_root())).replace("\\", "/")

    return None


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "completed_days" not in st.session_state:
    st.session_state.completed_days = set()

if "completed_exam_days" not in st.session_state:
    st.session_state.completed_exam_days = set()

if "completed_mock_days" not in st.session_state:
    st.session_state.completed_mock_days = set()

# Convert old lists to sets safely.
st.session_state.completed_days = set(st.session_state.completed_days)
st.session_state.completed_exam_days = set(
    st.session_state.completed_exam_days
)
st.session_state.completed_mock_days = set(
    st.session_state.completed_mock_days
)


# ---------------------------------------------------------
# UNLOCK LOGIC
# ---------------------------------------------------------
def is_day_unlocked(day_number: int) -> bool:
    """Check whether this specific roadmap day is available."""

    # Day 01 is always unlocked.
    if day_number == 1:
        return True

    # Assessment unlocks after its preceding four lessons.
    if day_number in EXAM_DAYS:
        return all(
            lesson_day in st.session_state.completed_days
            for lesson_day in required_lessons_for_exam(day_number)
        )

    # Mock Interview unlocks only after assessment is passed.
    if day_number in MOCK_INTERVIEW_DAYS:
        return (day_number - 1) in st.session_state.completed_exam_days

    # First lesson of a new cycle unlocks after mock interview completion.
    if (day_number - 1) in MOCK_INTERVIEW_DAYS:
        return (day_number - 1) in st.session_state.completed_mock_days

    # Every other lesson unlocks after its previous lesson is completed.
    return (day_number - 1) in st.session_state.completed_days


def status_for_day(day_number: int) -> tuple[str, str]:
    """Return the correct icon and status for each card."""

    if day_number in EXAM_DAYS:
        if day_number in st.session_state.completed_exam_days:
            return "✅", "Assessment passed"
        if is_day_unlocked(day_number):
            return "📝", "Ready to start"
        return "🔒", "Complete previous lessons"

    if day_number in MOCK_INTERVIEW_DAYS:
        if day_number in st.session_state.completed_mock_days:
            return "✅", "Interview completed"
        if is_day_unlocked(day_number):
            return "🎤", "Ready to start"
        return "🔒", "Pass the assessment first"

    if day_number in st.session_state.completed_days:
        return "✅", "Lesson completed"

    if is_day_unlocked(day_number):
        return "📘", "Ready to learn"

    return "🔒", "Locked"


# ---------------------------------------------------------
# PAGE DESIGN
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .hero {
            padding: 1.7rem 2rem;
            border-radius: 18px;
            color: white;
            background: linear-gradient(135deg, #1d4ed8 0%, #6d28d9 100%);
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2.1rem;
        }

        .hero p {
            margin: 0.45rem 0 0;
            opacity: 0.9;
            font-size: 1rem;
        }

        .progress-card {
            padding: 1rem;
            background: #f8fafc;
            border: 1px solid #dbe3ee;
            border-radius: 14px;
            text-align: center;
        }

        .progress-card h3 {
            margin: 0;
            color: #1e293b;
            font-size: 1.6rem;
        }

        .progress-card p {
            margin: 0.3rem 0 0;
            color: #64748b;
            font-size: 0.9rem;
        }

        .cycle-title {
            margin-top: 1.7rem;
            margin-bottom: 0.8rem;
            padding: 0.75rem 1rem;
            border-left: 5px solid #4f46e5;
            border-radius: 8px;
            background: #eef2ff;
            color: #312e81;
            font-weight: 700;
        }

        .day-type {
            margin: 0;
            color: #6366f1;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.06em;
        }

        .day-title {
            margin: 0.35rem 0 0;
            color: #0f172a;
            font-size: 1.15rem;
            font-weight: 700;
        }

        .day-status {
            margin: 0.4rem 0 0.75rem;
            color: #64748b;
            min-height: 2.6rem;
            font-size: 0.88rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>📚 Learning Portal</h1>
        <p>Your structured learning journey from lessons to assessments and mock interviews.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

lesson_count = len(st.session_state.completed_days)
exam_count = len(st.session_state.completed_exam_days)
mock_count = len(st.session_state.completed_mock_days)
overall_count = lesson_count + exam_count + mock_count

card1, card2, card3, card4 = st.columns(4)

with card1:
    st.markdown(
        f"""
        <div class="progress-card">
            <h3>{lesson_count}/24</h3>
            <p>Lessons Completed</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card2:
    st.markdown(
        f"""
        <div class="progress-card">
            <h3>{exam_count}/6</h3>
            <p>Assessments Passed</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card3:
    st.markdown(
        f"""
        <div class="progress-card">
            <h3>{mock_count}/6</h3>
            <p>Mock Interviews</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card4:
    st.markdown(
        f"""
        <div class="progress-card">
            <h3>{overall_count}/36</h3>
            <p>Overall Progress</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.subheader("🗺️ 36-Day Learning Roadmap")
st.caption(
    "Finish each stage to unlock the next lesson, assessment, or mock interview."
)


# ---------------------------------------------------------
# PROFESSIONAL ROADMAP CARDS
# ---------------------------------------------------------
for start_day in range(1, TOTAL_DAYS + 1, 6):
    cycle_number = ((start_day - 1) // 6) + 1
    end_day = min(start_day + 5, TOTAL_DAYS)

    st.markdown(
        f"""
        <div class="cycle-title">
            Learning Cycle {cycle_number} &nbsp;·&nbsp; Days {start_day:02d}–{end_day:02d}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two rows, three professional cards in each row.
    for row_start in range(start_day, end_day + 1, 3):
        columns = st.columns(3)

        row_end = min(row_start + 3, end_day + 1)

        for position, day_number in enumerate(range(row_start, row_end)):
            icon, status = status_for_day(day_number)
            unlocked = is_day_unlocked(day_number)

            if day_number in EXAM_DAYS:
                activity_type = "Assessment"
                button_label = "Start Assessment"

            elif day_number in MOCK_INTERVIEW_DAYS:
                activity_type = "AI Mock Interview"
                button_label = "Start Mock Interview"

            else:
                activity_type = "Learning Lesson"
                button_label = "Open Lesson"

            with columns[position]:
                with st.container(border=True):
                    st.markdown(
                        f'<p class="day-type">{activity_type}</p>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f'<p class="day-title">{icon} {day_label(day_number)}</p>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f'<p class="day-status">{status}</p>',
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        button_label,
                        key=f"roadmap_day_{day_number}",
                        disabled=not unlocked,
                        use_container_width=True,
                    ):
                        # Assessment card
                        if day_number in EXAM_DAYS:
                            st.session_state.selected_exam_day = day_number
                            st.switch_page("pages/AI_Exam.py")
                        # Mock interview card
                        elif day_number in MOCK_INTERVIEW_DAYS:
                            st.session_state.selected_mock_day = day_number
                            mock_page = find_activity_page("mock")

                            if mock_page:
                                st.switch_page(mock_page)

                            st.error("Mock Interview page was not found.")

                        # Normal lesson card
                        else:
                            st.session_state.selected_lesson_day = day_number
                            st.switch_page("pages/Lesson_View.py")