import streamlit as st
import sqlite3
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()


st.set_page_config(
    page_title="Announcement",
    page_icon="📢",
    layout="wide"
)


def get_connection():
    return sqlite3.connect("talent_sphere.db")


st.title("📢 Announcements")


st.subheader("Add Announcement")


message = st.text_area(
    "Announcement Message"
)


if st.button("Publish Announcement"):

    if message:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO announcements(message)
            VALUES (?)
            """,
            (message,)
        )

        conn.commit()
        conn.close()

        st.success(
            "✅ Announcement published successfully"
        )

    else:

        st.warning(
            "Please enter announcement"
        )


st.divider()


st.subheader("📢 Previous Announcements")


conn = get_connection()
cursor = conn.cursor()


cursor.execute(
    "SELECT message FROM announcements ORDER BY id DESC"
)


data = cursor.fetchall()


conn.close()


if data:

    for item in data:

        st.info(
            f"📢 {item[0]}"
        )

else:

    st.write(
        "No announcements available"
    )