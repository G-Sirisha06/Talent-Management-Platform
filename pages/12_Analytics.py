import streamlit as st
import sqlite3
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()

st.set_page_config(
    page_title="Analytics",
    page_icon="📊"
)


st.title("📊 Analytics Dashboard")


# Database connection
conn = sqlite3.connect("talent_sphere.db")
cursor = conn.cursor()


# Total Users
cursor.execute(
    "SELECT COUNT(*) FROM users"
)
total_users = cursor.fetchone()[0]


# Total Exams
cursor.execute(
    "SELECT COUNT(*) FROM exams"
)
total_exams = cursor.fetchone()[0]


# Total Announcements
cursor.execute(
    "SELECT COUNT(*) FROM announcements"
)
total_announcements = cursor.fetchone()[0]


conn.close()



# Metrics

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "👥 Total Users",
        total_users
    )


with col2:
    st.metric(
        "📝 Total Exams",
        total_exams
    )


with col3:
    st.metric(
        "📢 Announcements",
        total_announcements
    )



st.divider()


st.subheader("📈 Platform Activity")


chart_data = {
    "Week 1": 20,
    "Week 2": 45,
    "Week 3": 65,
    "Week 4": 90
}


st.line_chart(chart_data)


st.success(
    "✅ Analytics loaded successfully"
)