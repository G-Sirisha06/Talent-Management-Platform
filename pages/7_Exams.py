import streamlit as st
import sqlite3
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()


st.set_page_config(
    page_title="Exams",
    page_icon="📝",
    layout="wide"
)


# Database Connection

def get_connection():
    return sqlite3.connect("talent_sphere.db")



st.title("📝 Online Exams")

st.write(
    "Attempt available exams and check your score."
)



# Fetch Exams

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


    exam_id = exam_dict[selected_exam]


    # Fetch Questions

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT question, option1, option2, option3, option4, answer
        FROM questions
        WHERE exam_id=?
        """,
        (exam_id,)
    )


    questions = cursor.fetchall()


    conn.close()



    if questions:


        st.subheader(
            f"📚 {selected_exam}"
        )


        answers = []


        for i, q in enumerate(questions):


            st.write(
                f"**{i+1}. {q[0]}**"
            )


            selected = st.radio(
                "Choose Answer",
                [
                    q[1],
                    q[2],
                    q[3],
                    q[4]
                ],
                key=i
            )


            answers.append(selected)



        if st.button("Submit Exam"):


            score = 0


            for i, ans in enumerate(answers):

                correct_option = questions[i][5]

                options = [
                    questions[i][1],
                    questions[i][2],
                    questions[i][3],
                    questions[i][4]
                ]

                correct_answer = options[
                    int(correct_option[-1])-1
                ]

                if ans == correct_answer:
                    score += 1


            st.success(
                f"Your Score: {score}/{len(questions)}"
            )


            percentage = (
                score / len(questions)
            ) * 100



            if percentage >= 70:

                st.balloons()

                st.success(
                    "Excellent Performance 🎉"
                )

            else:

                st.warning(
                    "Keep Practicing 👍"
                )



    else:

        st.info(
            "No questions available for this exam."
        )


else:

    st.warning(
        "No exams available. Please check later."
    )