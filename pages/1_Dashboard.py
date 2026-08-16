import streamlit as st
import sqlite3
import random
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()


st.set_page_config(
    page_title="User Dashboard",
    page_icon="🏠",
    layout="wide"
)


# =====================
# SESSION CHECK
# =====================

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None


if not st.session_state["authenticated"]:
    st.warning("Please login first")
    st.stop()


if st.session_state["user_role"] != "User":
    st.warning("Access denied")
    st.stop()



DB = "talent_sphere.db"
def get_chat_count():

    try:
        conn = sqlite3.connect(DB)

        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM chat_history"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    except Exception as e:
        return 0
chats=get_chat_count()  # Function to get the count of AI chats


# =====================
# DATABASE FUNCTIONS
# =====================

def get_count(table):

    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        result = cursor.fetchone()[0]

        conn.close()

        return result

    except:
        return 0
import os

def get_document_count():

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    upload_dir = os.path.join(
        BASE_DIR,
        "data",
        "uploads"
    )

    if not os.path.exists(upload_dir):
        return 0

    pdf_files = [
        f for f in os.listdir(upload_dir)
        if f.endswith(".pdf")
    ]
    
    return len(pdf_files)


def get_announcements():

    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT message 
            FROM announcements
            ORDER BY id DESC
            LIMIT 5
            """
        )

        data = cursor.fetchall()

        conn.close()

        return data

    except:
        return []



# def get_exams():

#     try:
#         conn = sqlite3.connect(DB)
#         cursor = conn.cursor()

#         cursor.execute(
#             """
#             SELECT *
#             FROM exams
#             LIMIT 5
#             """
#         )

#         data = cursor.fetchall()

#         conn.close()

#         return data

#     except:
#         return []

def get_exams():

    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT exam_name
            FROM exams
            LIMIT 5
            """
        )

        data = cursor.fetchall()

        conn.close()

        return data

    except Exception:
        return []

# =====================
# CSS
# =====================

st.markdown(
"""
<style>

.hero{

background:linear-gradient(135deg,#2563eb,#7c3aed);
padding:35px;
border-radius:20px;
color:white;

}


.card{

background:white;
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0 4px 15px rgba(0,0,0,0.1);

}


.section{

font-size:24px;
font-weight:700;
margin-top:25px;

}


.tip{

background:#f1f5f9;
padding:20px;
border-radius:15px;

}


</style>
""",
unsafe_allow_html=True
)



# =====================
# SIDEBAR
# =====================

with st.sidebar:

    st.title("🚀 Talent Management Platform")

    st.write(
        "👤 User Dashboard"
    )

    st.divider()


    if st.button("🤖 AI Chatbot"):

        st.switch_page(
            "pages/9_User_Chatbot.py"
        )


    if st.button("📄 Resume Analyzer"):

        st.switch_page(
            "pages/3_Resume_Analyser.py"
        )


    if st.button("📚 Learning Resources"):

        st.switch_page(
            "pages/14_Document.py"
        )


    if st.button("📝 Exams"):

        st.switch_page(
            "pages/7_Exams.py"
        )
    if st.button("🔍 Search"):

            st.switch_page(
                "pages/6_Semantic_Search.py"
            )
    if st.button("Learning Portal"):

            st.switch_page(
                "pages/16_Learning_portal.py"
            )


    st.divider()


    if st.button("Logout 🚪"):

        st.session_state["authenticated"] = False
        st.session_state["user_role"] = None

        st.switch_page("app.py")




# =====================
# HERO
# =====================

st.markdown(
f"""

<div class="hero">

<h1>🚀 Welcome User 👋</h1>

<h3>
AI Powered Career Preparation Platform
</h3>

<p>
Learn • Practice • Improve • Grow
</p>

</div>

""",
unsafe_allow_html=True
)



# =====================
# STATISTICS
# =====================


documents = get_document_count()

exams = get_count("exams")
chats = get_chat_count()  # Function to get the count of AI chats


st.markdown(
"## 📊 Your Learning Statistics"
)



c1,c2,c3,c4 = st.columns(4)


with c1:
    st.metric(
        "📚 Documents",
        documents
    )


with c2:
    st.metric(
        "🤖 AI Chats",
        chats
    )


with c3:
    st.metric(
        "📝 Exams",
        exams
    )


with c4:
    st.metric(
        "🏆 Progress",
        "65%"
    )



# =====================
# QUICK ACTIONS
# =====================


st.markdown(
"## ⚡ Quick Actions"
)


a,b,c,d = st.columns(4)


with a:

    if st.button("🤖 AI Chatbot"):

        st.switch_page(
            "pages/9_User_Chatbot.py"
        )


with b:

    if st.button("📄 Resume"):

        st.switch_page(
            "pages/3_Resume_Analyser.py"
        )


with c:

    if st.button("📚 Resources"):

        st.switch_page(
            "pages/14_Document.py"
        )


with d:

    if st.button("📝 Exam"):

        st.switch_page(
            "pages/7_Exams.py"
        )

def get_chat_count():

    try:
        conn = sqlite3.connect(DB)

        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM chat_history"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    except:
        return 0

# =====================
# ANNOUNCEMENTS
# =====================


st.markdown(
"## 📢 Latest Announcements"
)


announcements = get_announcements()


if announcements:

    for item in announcements:

        st.info(
            "📢 "+item[0]
        )

else:

    st.write(
        "No announcements available"
    )



# =====================
# UPCOMING EXAMS
# =====================


# st.markdown(
# "## 📅 Upcoming Exams"
# )


# exam_list = get_exams()


# if exam_list:

#     for exam in exam_list:

#         st.write(
#             f"📝 {exam}"
#         )

# else:

#     st.write(
#         "No exams scheduled"
#     )

# =====================
# UPCOMING EXAMS
# =====================

st.markdown("## 📅 Upcoming Exams")

exam_list = get_exams()

if exam_list:

    for exam in exam_list:

        st.info(
            f"📝 {exam[0]}"
        )

else:

    st.info(
        "📭 No upcoming exams available."
    )

# =====================
# PROGRESS
# =====================


st.markdown(
"## 📈 Learning Progress"
)


st.progress(65)


st.success(
"65% Course Completion"
)



# =====================
# AI TIP
# =====================


tips = [

"Practice Python daily 🚀",

"Learn SQL for data jobs 📊",

"Build projects for your resume 💻",

"Revise ML algorithms regularly 🤖",

"Improve communication skills 🎯"

]


st.markdown(
"## 💡 Today's AI Tip"
)


st.info(
random.choice(tips)
)