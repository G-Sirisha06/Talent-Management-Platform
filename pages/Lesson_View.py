"""Talent Sphere Elevate - Lesson PDF Viewer."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Lesson Viewer",
    page_icon="📘",
    layout="wide",
)

# Change this only if your portal file has a different name.
LEARNING_PORTAL_PAGE = "pages/16_Learning_portal.py"


def project_root() -> Path:
    """Find the project root containing Documents and pages."""
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


def pdf_files_for(day_number: int) -> list[Path]:
    """Read PDF files from Documents/Day_XX."""
    folder = project_root() / "Documents" / f"Day_{day_number:02d}"

    if not folder.exists():
        return []

    return sorted(
        [
            file
            for file in folder.iterdir()
            if file.is_file() and file.suffix.lower() == ".pdf"
        ],
        key=lambda file: file.name.lower(),
    )


def show_pdf(pdf_file: Path) -> None:
    """Display PDF directly in the separate lesson page."""
    pdf_base64 = base64.b64encode(pdf_file.read_bytes()).decode("utf-8")

    st.markdown(
        f"""
        <iframe
            src="data:application/pdf;base64,{pdf_base64}"
            width="100%"
            height="760"
            style="border: 1px solid #dbe3ee; border-radius: 14px;"
        ></iframe>
        """,
        unsafe_allow_html=True,
    )


if "completed_days" not in st.session_state:
    st.session_state.completed_days = set()

st.session_state.completed_days = set(st.session_state.completed_days)

selected_day = st.session_state.get("selected_lesson_day")

st.markdown(
    """
    <style>
        .lesson-hero {
            padding: 1.4rem 1.7rem;
            border-radius: 16px;
            color: white;
            background: linear-gradient(135deg, #0f766e, #2563eb);
            margin-bottom: 1.25rem;
        }

        .lesson-hero h1 {
            margin: 0;
            font-size: 1.8rem;
        }

        .lesson-hero p {
            margin: 0.35rem 0 0;
            opacity: 0.9;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if not selected_day:
    st.warning("No lesson has been selected.")

    if st.button("← Back to Learning Portal"):
        st.switch_page(LEARNING_PORTAL_PAGE)

    st.stop()

st.markdown(
    f"""
    <div class="lesson-hero">
        <h1>📘 {day_label(selected_day)} Learning Material</h1>
        <p>Read the material below, then mark this lesson as completed.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("← Back to Learning Portal"):
    st.switch_page(LEARNING_PORTAL_PAGE)

lesson_pdfs = pdf_files_for(selected_day)

if not lesson_pdfs:
    st.warning(
        f"No PDF found for {day_label(selected_day)}. "
        f"Please add a PDF in Documents/Day_{selected_day:02d}."
    )
    st.stop()

if len(lesson_pdfs) > 1:
    selected_pdf_name = st.selectbox(
        "Select Learning PDF",
        options=[pdf.name for pdf in lesson_pdfs],
    )

    selected_pdf = next(
        pdf for pdf in lesson_pdfs if pdf.name == selected_pdf_name
    )

else:
    selected_pdf = lesson_pdfs[0]

show_pdf(selected_pdf)

st.divider()

if selected_day in st.session_state.completed_days:
    st.success(
        f"✅ {day_label(selected_day)} is completed. "
        "Your next lesson is now available."
    )

else:
    if st.button(
        f"✅ Mark {day_label(selected_day)} as Completed",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.completed_days.add(selected_day)
        st.success(
            f"{day_label(selected_day)} completed successfully. "
            "You can now continue to the next stage."
        )

if st.button(
    "Continue to Learning Portal",
    use_container_width=True,
):
    st.switch_page(LEARNING_PORTAL_PAGE)