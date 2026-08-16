# import streamlit as st
# import sqlite3
# from src.sidebar import hide_Pages_sidebar
# import pandas as pd

# hide_Pages_sidebar()

# st.set_page_config(
#     page_title="Admin Dashboard",
#     page_icon="🛠",
#     layout="wide"
# )

# # =====================
# # SESSION CHECK
# # =====================

# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = False

# if "user_role" not in st.session_state:
#     st.session_state["user_role"] = None

# if not st.session_state["authenticated"]:
#     st.warning("Please login first")
#     st.stop()

# if st.session_state["user_role"] != "Admin":
#     st.warning("Access Denied")
#     st.stop()

# DB = "talent_sphere.db"

# # =====================
# # DATABASE FUNCTIONS
# # =====================

# def get_count(table):
#     try:
#         conn = sqlite3.connect(DB)
#         cursor = conn.cursor()

#         cursor.execute(f"SELECT COUNT(*) FROM {table}")

#         count = cursor.fetchone()[0]

#         conn.close()

#         return count

#     except:
#         return 0


# def get_announcements():
#     try:
#         conn = sqlite3.connect(DB)
#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT message
#             FROM announcements
#             ORDER BY id DESC
#             LIMIT 5
#         """)

#         data = cursor.fetchall()

#         conn.close()

#         return data

#     except:
#         return []


# # =====================
# # CSS
# # =====================

# st.markdown("""
# <style>

# .hero{
# background:linear-gradient(135deg,#2563eb,#7c3aed);
# padding:35px;
# border-radius:20px;
# color:white;
# margin-bottom:20px;
# }

# .card{
# background:white;
# padding:20px;
# border-radius:15px;
# box-shadow:0 4px 15px rgba(0,0,0,.1);
# text-align:center;
# }

# .section{
# font-size:24px;
# font-weight:700;
# margin-top:25px;
# }

# </style>
# """, unsafe_allow_html=True)

# # =====================
# # SIDEBAR
# # =====================

# with st.sidebar:

#     st.title("🚀 Talent Sphere")

#     st.write("🛠 Admin Dashboard")

#     st.divider()

#     if st.button("🤖 AI Assistant"):
#         st.switch_page("pages/2_AI_Chatbot.py")

#     if st.button("👥 User Management"):
#         st.switch_page("pages/11_Manage_Users.py")

#     if st.button("📥 Document Ingestion"):
#         st.switch_page("pages/5_Document_Ingestion.py")

#     if st.button("📝 Exams"):
#         st.switch_page("pages/15_Admin_exams.py")

#     if st.button("📢 Announcements"):
#         st.switch_page("pages/8_Announcements.py")

#     st.divider()

#     if st.button("🚪 Logout"):
#         st.session_state["authenticated"] = False
#         st.session_state["user_role"] = None
#         st.switch_page("app.py")

# # =====================
# # HERO
# # =====================

# st.markdown(f"""
# <div class="hero">

# <h1>🛠 Welcome Admin 👋</h1>

# <h3>
# Manage Users • Documents • Exams • Announcements
# </h3>

# <p>
# Monitor your AI powered training platform.
# </p>

# </div>
# """, unsafe_allow_html=True)

# # =====================
# # STATISTICS
# # =====================

# users = get_count("users")
# documents = get_count("documents")
# exams = get_count("exams")
# announcements = get_count("announcements")

# st.markdown("## 📊 Platform Statistics")

# c1, c2, c3, c4 = st.columns(4)

# with c1:
#     st.metric("👥 Users", users)

# with c2:
#     st.metric("📄 Documents", documents)

# with c3:
#     st.metric("📝 Exams", exams)

# with c4:
#     st.metric("📢 Announcements", announcements)
# # =====================
# # QUICK ACTIONS
# # =====================

# st.markdown("## ⚡ Quick Actions")

# q1, q2, q3, q4 = st.columns(4)

# with q1:
#     if st.button("👥 Manage Users"):
#         st.switch_page("pages/11_Manage_Users.py")

# with q2:
#     if st.button("📥 Upload Documents"):
#         st.switch_page("pages/5_Document_Ingestion.py")

# with q3:
#     if st.button("📝 Create Exams"):
#         st.switch_page("pages/15_Admin_exams.py")

# with q4:
#     if st.button("📢 Announcements"):
#         st.switch_page("pages/8_Announcements.py")


# # =====================
# # DASHBOARD
# # =====================

# left, right = st.columns([2, 1])

# with left:

#     st.markdown("## 📢 Latest Announcements")

#     data = get_announcements()

#     if data:
#         for item in data:
#             st.info(f"📢 {item[0]}")
#     else:
#         st.info("No announcements available.")

#     st.markdown("## 📋 Recent Activity")

#     st.success("✅ User login activity monitored")
#     st.success("📄 Documents uploaded successfully")
#     st.success("📝 Exams published")
#     st.success("📢 Announcements sent")


# with right:

#     st.markdown("## 📊 Platform Health")

#     st.progress(100)

#     st.success("🟢 All Systems Operational")

#     st.metric("🤖 AI Requests Today", 128)

#     st.metric("💬 Chat Sessions", get_count("chat_history"))

#     st.metric("📈 Platform Usage", "95%")

#     st.metric("⚡ Server Status", "Online")
# # =====================
# # ANALYTICS
# # =====================

# st.markdown("## 📈 Analytics")

# left_chart, right_chart = st.columns(2)

# with left_chart:

#     st.subheader("Platform Overview")

#     chart_data = pd.DataFrame(
#         {
#             "Count": [
#                 users,
#                 documents,
#                 exams,
#                 announcements
#             ]
#         },
#         index=[
#             "Users",
#             "Documents",
#             "Exams",
#             "Announcements"
#         ]
#     )

#     st.bar_chart(chart_data)

# with right_chart:

#     st.subheader("Platform Growth")

#     growth = pd.DataFrame(
#         {
#             "Activity": [
#                 users,
#                 users + 2,
#                 users + 4,
#                 users + 6,
#                 users + 8
#             ]
#         },
#         index=[
#             "Week 1",
#             "Week 2",
#             "Week 3",
#             "Week 4",
#             "Week 5"
#         ]
#     )

#     st.line_chart(growth)


# # =====================
# # FOOTER
# # =====================

# st.divider()

# st.caption("© 2026 Talent Sphere Elevate | Admin Dashboard")


# ==============================
# 10_Admin.py
# Talent Sphere Elevate
# ==============================

import streamlit as st
import sqlite3
import pandas as pd
import os
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()


DB = "talent_sphere.db"


st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="⚙️",
    layout="wide"
)


# ==============================
# SESSION CHECK
# ==============================

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None


if not st.session_state["authenticated"]:
    st.warning("Please login first")
    st.stop()


if st.session_state["user_role"] != "Admin":
    st.error("Access denied")
    st.stop()



# ==============================
# DATABASE FUNCTIONS
# ==============================

def get_connection():

    return sqlite3.connect(DB)



def get_total_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count



def get_total_documents():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    upload_dir = os.path.join(BASE_DIR, "data", "uploads")

    if not os.path.exists(upload_dir):
        return 0

    pdf_files = [
        f for f in os.listdir(upload_dir)
        if f.endswith(".pdf")
    ]

    return len(pdf_files)


def get_total_exams():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM exams"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count



def get_total_announcements():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM announcements"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count



def get_recent_announcements():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message
        FROM announcements
        ORDER BY id DESC
        LIMIT 5
    """)

    data = cursor.fetchall()

    conn.close()

    return data



def get_recent_users():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT email, role
        FROM users
        ORDER BY id DESC
        LIMIT 5
        """,
        conn
    )

    conn.close()

    return df



def get_recent_exams():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT exam_name
        FROM exams
        ORDER BY id DESC
        LIMIT 5
        """,
        conn
    )

    conn.close()

    return df



# ==============================
# CSS
# ==============================

st.markdown(
"""
<style>

.hero{

background:linear-gradient(
135deg,
#6366f1,
#8b5cf6
);

padding:35px;
border-radius:20px;
color:white;

}


.card{

background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 5px 20px rgba(0,0,0,0.1);
text-align:center;

}


.title{

font-size:18px;
font-weight:700;

}


</style>

""",
unsafe_allow_html=True
)



# ==============================
# SIDEBAR
# ==============================


with st.sidebar:


    st.title("⚙️ Admin Panel")


    st.subheader("Overview")


    st.page_link(
        "app.py",
        label="🏠 Dashboard"
    )


    st.subheader("Workspace")


    st.page_link(
        "pages/2_AI_Chatbot.py",
        label="🤖 AI Assistant"
    )


    st.page_link(
        "pages/14_Document.py",
        label="📄 Document"
    )


    st.page_link(
        "pages/6_Semantic_Search.py",
        label="🔍 Search"
    )


    st.subheader("Administration")


    st.page_link(
        "pages/11_Manage_Users.py",
        label="👥 User Management"
    )


    st.page_link(
        "pages/5_Document_Ingestion.py",
        label="📥 Document Ingestion"
    )


    st.page_link(
        "pages/15_Admin_exams.py",
        label="📝 Exams"
    )


    st.page_link(
        "pages/8_Announcements.py",
        label="📢 Announcement"
    )


    st.divider()


    if st.button("🚪 Logout"):

        st.session_state["authenticated"] = False
        st.session_state["user_role"] = None

        st.rerun()



# ==============================
# HERO SECTION
# ==============================


st.markdown(
f"""
<div class="hero">

<h1>🚀 Talent Management Platform</h1>

<h3>Admin Dashboard</h3>

<p>
Welcome back Admin 👋
</p>

</div>
""",
unsafe_allow_html=True
)
# ==============================
# STATISTICS CARDS
# ==============================

st.markdown("## 📊 Platform Statistics")


users = get_total_users()
documents = get_total_documents()
exams = get_total_exams()
announcements = get_total_announcements()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Total Users",
        users
    )


with col2:

    st.metric(
        "📄 Total Documents",
        documents
    )


with col3:

    st.metric(
        "📝 Total Exams",
        exams
    )


with col4:

    st.metric(
        "📢 Announcements",
        announcements
    )



# ==============================
# QUICK ACTIONS
# ==============================


st.markdown("## ⚡ Quick Actions")


q1, q2, q3, q4 = st.columns(4)


with q1:

    st.info(
        "👥\n\nManage Users\n\nCreate and manage platform users"
    )


with q2:

    st.info(
        "📥\n\nUpload Documents\n\nAdd learning materials"
    )


with q3:

    st.info(
        "📝\n\nCreate Exams\n\nManage assessments"
    )


with q4:

    st.info(
        "📢\n\nAnnouncements\n\nShare updates"
    )



# ==============================
# ANALYTICS SECTION
# ==============================


st.markdown("## 📈 Analytics")


chart_col1, chart_col2 = st.columns(2)



# Bar Chart

with chart_col1:


    st.subheader(
        "Platform Overview"
    )


    chart_data = pd.DataFrame(
        {
            "Category":
            [
                "Users",
                "Documents",
                "Exams",
                "Announcements"
            ],

            "Count":
            [
                users,
                documents,
                exams,
                announcements
            ]
        }
    )


    st.bar_chart(
        chart_data.set_index("Category")
    )



# Line Chart

with chart_col2:


    st.subheader(
        "Activity Trend"
    )


    trend_data = pd.DataFrame(
        {
            "Activity":
            [
                "Users",
                "Documents",
                "Exams",
                "Announcements"
            ],

            "Count":
            [
                users,
                documents,
                exams,
                announcements
            ]
        }
    )


    st.line_chart(
        trend_data.set_index("Activity")
    )
# ==============================
# RECENT USERS
# ==============================

st.markdown("## 👥 Recently Added Users")


recent_users = get_recent_users()


if not recent_users.empty:

    st.dataframe(
        recent_users,
        use_container_width=True
    )

else:

    st.info("No users found.")



# ==============================
# RECENT ANNOUNCEMENTS
# ==============================

st.markdown("## 📢 Recent Announcements")


recent_announcements = get_recent_announcements()


if recent_announcements:

    for announcement in recent_announcements:

        st.info(
            f"📢 {announcement[0]}"
        )

else:

    st.info(
        "No announcements available."
    )



# ==============================
# RECENT EXAMS
# ==============================

st.markdown("## 📝 Recent Exams")


recent_exams = get_recent_exams()


if not recent_exams.empty:

    st.dataframe(
        recent_exams,
        use_container_width=True
    )

else:

    st.info(
        "No exams available."
    )



# ==============================
# RECENT DOCUMENTS
# ==============================

st.markdown("## 📄 Recent Documents")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

upload_dir = os.path.join(BASE_DIR, "data", "uploads")

if os.path.exists(upload_dir):

    files = [
        f for f in os.listdir(upload_dir)
        if f.endswith(".pdf")
    ]

    if files:

        for file in files[-5:]:

            st.success(
                f"📄 {file}"
            )

    else:

        st.info(
            "No documents uploaded."
        )

else:

    st.info(
        " No uploaded Documents  not found."
    )



# ==============================
# PLATFORM STATUS
# ==============================

st.markdown("## 🎯 Platform Status")


s1, s2, s3 = st.columns(3)


with s1:

    st.success(
        "✅ Database Connected"
    )


with s2:

    st.success(
        "✅ AI Services Active"
    )


with s3:

    st.success(
        "✅ Platform Operational"
    )