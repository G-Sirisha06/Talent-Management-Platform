# import streamlit as st
# import sqlite3
# from src.sidebar import hide_Pages_sidebar
# hide_Pages_sidebar()

# st.set_page_config(
#     page_title="User Management",
#     page_icon="👥",
#     layout="wide"
# )


# def get_connection():
#     return sqlite3.connect("talent_sphere.db")


# st.title("👥 User Management")


# # ---------------- ADD USER ----------------

# st.subheader("➕ Add New User")


# email = st.text_input(
#     "Email Address"
# )

# password = st.text_input(
#     "Password",
#     type="password"
# )


# role = st.selectbox(
#     "Select Role",
#     [
#         "User",
#         "Admin"
#     ]
# )


# if st.button("Create User"):

#     if email and password:

#         conn = get_connection()
#         cursor = conn.cursor()


#         try:

#             cursor.execute(
#                 """
#                 INSERT INTO users(email, password, role)
#                 VALUES (?, ?, ?)
#                 """,
#                 (
#                     email,
#                     password,
#                     role
#                 )
#             )


#             conn.commit()

#             st.success(
#                 "✅ User created successfully"
#             )


#         except sqlite3.IntegrityError:

#             st.error(
#                 "❌ User already exists"
#             )


#         conn.close()


#     else:

#         st.warning(
#             "Please fill all details"
#         )



# st.divider()



# # ---------------- VIEW USERS ----------------

# st.subheader("👥 Existing Users")


# conn = get_connection()
# cursor = conn.cursor()


# cursor.execute(
#     "SELECT email, role FROM users"
# )


# users = cursor.fetchall()


# conn.close()



# if users:

#     for user in users:

#         col1, col2 = st.columns(2)


#         with col1:
#             st.write(
#                 f"📧 {user[0]}"
#             )


#         with col2:
#             st.write(
#                 f"👤 {user[1]}"
#             )

# else:

#     st.info(
#         "No users available"
#     )





import streamlit as st
import sqlite3
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

from src.sidebar import hide_Pages_sidebar


# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

hide_Pages_sidebar()


# -----------------------------------------
# LOAD .ENV
# -----------------------------------------

load_dotenv()


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def get_connection():
    return sqlite3.connect("talent_sphere.db")


# -----------------------------------------
# SEND EMAIL FUNCTION
# -----------------------------------------

def send_credentials_email(
    recipient_email,
    password,
    role
):

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:

        return False, "Email configuration is missing in .env file."

    try:

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = recipient_email
        message["Subject"] = "Talent Sphere Elevate - Login Credentials"


        body = f"""
Hello,

Welcome to Talent Sphere Elevate! 🚀

Your account has been successfully created by the administrator.

Login Details
--------------------------------

Email    : {recipient_email}
Password : {password}
Role     : {role}

You can use these credentials to sign in to Talent Sphere Elevate.

Please keep your password safe and do not share it with anyone.

Best Regards,
Talent Sphere Elevate Team
"""


        message.attach(
            MIMEText(body, "plain")
        )


        # Gmail SMTP server
        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            recipient_email,
            message.as_string()
        )

        server.quit()


        return True, "Email sent successfully."


    except Exception as e:

        return False, str(e)


# -----------------------------------------
# PAGE TITLE
# -----------------------------------------

st.title("👥 User Management")

st.write(
    "Create users and automatically send their login credentials by email."
)


# -----------------------------------------
# ADD USER
# -----------------------------------------

st.subheader("➕ Add New User")


email = st.text_input(
    "Email Address",
    placeholder="user@gmail.com"
)


password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter password"
)


role = st.selectbox(
    "Select Role",
    [
        "User",
        "Admin"
    ]
)


# -----------------------------------------
# CREATE USER
# -----------------------------------------

if st.button(
    "Create User",
    type="primary"
):

    if not email or not password:

        st.warning(
            "⚠️ Please fill all details."
        )

    else:

        conn = get_connection()
        cursor = conn.cursor()

        try:

            # -----------------------------
            # CREATE USER IN DATABASE
            # -----------------------------

            cursor.execute(
                """
                INSERT INTO users(email, password, role)
                VALUES (?, ?, ?)
                """,
                (
                    email,
                    password,
                    role
                )
            )

            conn.commit()

            # -----------------------------
            # SEND EMAIL
            # -----------------------------

            email_sent, message = send_credentials_email(
                email,
                password,
                role
            )


            # -----------------------------
            # SHOW RESULT
            # -----------------------------

            if email_sent:

                st.success(
                    "✅ User created successfully!"
                )

                st.success(
                    f"📧 Login credentials sent to {email}"
                )

            else:

                st.warning(
                    "⚠️ User was created, but email could not be sent."
                )

                st.error(
                    f"Email Error: {message}"
                )


        except sqlite3.IntegrityError:

            st.error(
                "❌ User already exists."
            )


        except Exception as e:

            st.error(
                f"❌ Error creating user: {e}"
            )


        finally:

            conn.close()


# -----------------------------------------
# DIVIDER
# -----------------------------------------

st.divider()


# -----------------------------------------
# EXISTING USERS
# -----------------------------------------

st.subheader("👥 Existing Users")


conn = get_connection()
cursor = conn.cursor()


cursor.execute(
    "SELECT email, role FROM users"
)


users = cursor.fetchall()


conn.close()


if users:

    for user in users:

        col1, col2 = st.columns(2)


        with col1:

            st.write(
                f"📧 {user[0]}"
            )


        with col2:

            st.write(
                f"👤 {user[1]}"
            )

else:

    st.info(
        "No users available."
    )