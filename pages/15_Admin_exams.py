import streamlit as st
import sqlite3
import json 
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()

st.set_page_config(
    page_title="Admin Exams",
    page_icon="📝",
    layout="wide"
)


def get_connection():
    return sqlite3.connect("talent_sphere.db")



st.title("📝 Admin Exam Management")


tab1, tab2 = st.tabs(
    [
        "➕ Create Exam",
        "❓ Add Questions"
    ]
)



# ================= CREATE EXAM =================

with tab1:

    st.subheader("➕ Create New Exam")


    exam_name = st.text_input(
        "Exam Name"
    )


    if st.button("Create Exam"):

        if exam_name:

            conn = get_connection()
            cursor = conn.cursor()


            cursor.execute(
                """
                INSERT INTO exams(exam_name)
                VALUES(?)
                """,
                (exam_name,)
            )


            conn.commit()
            conn.close()


            st.success(
                "✅ Exam created successfully"
            )

        else:

            st.warning(
                "Enter exam name"
            )



# ================= ADD QUESTIONS =================

with tab2:

    st.subheader("❓ Add Questions")


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM exams"
    )

    exams = cursor.fetchall()


    conn.close()



    if exams:


        exam_dict = {
            exam[1]: exam[0]
            for exam in exams
        }


        selected_exam = st.selectbox(
            "Select Exam",
            list(exam_dict.keys())
        )



        if "question_no" not in st.session_state:

            st.session_state.question_no = 1



        st.write(
            f"### Question {st.session_state.question_no}"
        )


        question = st.text_input(
            "Question"
        )


        option1 = st.text_input(
            "Option 1"
        )

        option2 = st.text_input(
            "Option 2"
        )

        option3 = st.text_input(
            "Option 3"
        )

        option4 = st.text_input(
            "Option 4"
        )


        answer = st.text_input(
            "Correct Answer"
        )



        col1, col2 = st.columns(2)



        with col1:


            if st.button("➕ Add Question"):


                if question and answer:


                    conn = get_connection()
                    cursor = conn.cursor()


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
                            exam_dict[selected_exam],
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer
                        )
                    )


                    conn.commit()
                    conn.close()


                    st.success(
                        "✅ Question added successfully"
                    )


                    st.session_state.question_no += 1


                    st.rerun()


                else:

                    st.warning(
                        "Enter question and answer"
                    )



        with col2:


            if st.button("🔄 Add Another Question"):

                st.session_state.question_no += 1

                st.rerun()



    else:

        st.info(
            "Create exam first"
        )