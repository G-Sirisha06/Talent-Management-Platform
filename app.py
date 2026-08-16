import streamlit as st
import sqlite3
import os
from PyPDF2 import PdfReader

# Page Configuration
st.set_page_config(
    page_title="Talent Management Platform",
    page_icon="🚀",
    layout="wide"
)
def get_dashboard_data():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    upload_dir = os.path.join(
        BASE_DIR,
        "data",
        "uploads"
    )

    document_count = 0
    total_pages = 0

    if os.path.exists(upload_dir):

        pdf_files = [
            f for f in os.listdir(upload_dir)
            if f.endswith(".pdf")
        ]

        document_count = len(pdf_files)

        for file in pdf_files:

            path = os.path.join(
                upload_dir,
                file
            )

            try:

                reader = PdfReader(path)

                total_pages += len(reader.pages)

            except Exception:

                pass

    conn = sqlite3.connect(
        "talent_sphere.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM exams"
    )

    exams = cursor.fetchone()[0]

    conn.close()

    return document_count, total_pages, exams
# 1. Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

# ==========================================
# SCREEN 1: LOGIN PAGE (Sidebar is HIDDEN)
# ==========================================
if not st.session_state["authenticated"]:
    # Custom CSS to hide default Streamlit elements ONLY on the Login page
    # st.markdown("""
    # <style>
    # /* Completely Hide Sidebar on Login */
    # [data-testid="stSidebar"] { display: none !important; }
    # [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    # #MainMenu { visibility: hidden; }
    # header { visibility: hidden; }
    # footer { visibility: hidden; }

    # :root {
    #     --primary-color: #6366f1;
    #     --primary-hover: #4f46e5;
    #     --logo-bg: #e0e7ff;
    #     --bg-card: #ffffff;
    #     --text-dark: #0f172a;
    #     --text-muted: #64748b;
    # }

    # .app-logo {
    #     font-size: 50px;
    #     margin-bottom: 15px;
    #     display: inline-block;
    #     background-color: var(--logo-bg);
    #     padding: 15px;
    #     border-radius: 18px;
    # }

    # .main-title {
    #     font-size: 26px;
    #     font-weight: 700;
    #     color: var(--text-dark);
    #     margin-bottom: 5px;
    # }

    # .sub-title {
    #     font-size: 14px;
    #     color: var(--text-muted);
    #     margin-bottom: 30px;
    # }

    # .signin-header {
    #     font-size: 20px;
    #     font-weight: 600;
    #     color: var(--text-dark);
    #     text-align: left;
    #     margin-bottom: 4px;
    # }

    # .admin-notice {
    #     font-size: 13px;
    #     color: var(--text-muted);
    #     text-align: left;
    #     margin-bottom: 20px;
    # }

    # .footer-note {
    #     font-size: 11px;
    #     color: #94a3b8;
    #     text-align: left;
    #     margin-top: 25px;
    #     line-height: 1.4;
    # }

    # div[data-baseweb="input"] {
    #     border-radius: 8px !important;
    #     border: 1px solid #cbd5e1 !important;
    # }

    # div[data-baseweb="input"]:focus-within {
    #     border-color: var(--primary-color) !important;
    # }

    # div.stButton > button {
    #     background-color: var(--primary-color) !important;
    #     color: white !important;
    #     font-weight: 600 !important;
    #     padding: 10px 24px !important;
    #     border-radius: 50px !important;
    #     border: none !important;
    #     width: 100% !important;
    #     transition: all 0.3s ease;
    # }

    # div.stButton > button:hover {
    #     background-color: var(--primary-hover) !important;
    #     box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    # }
    # </style>
    # """, unsafe_allow_html=True)
    st.markdown("""
    <style>

    /* ================================
    HIDE STREAMLIT DEFAULT UI
    ================================ */

    [data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ================================
    LOGIN PAGE BACKGROUND
    ================================ */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 15%,
                rgba(129, 140, 248, 0.45),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 85%,
                rgba(236, 72, 153, 0.35),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 10%,
                rgba(45, 212, 191, 0.25),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #eef2ff 0%,
                #f8fafc 45%,
                #fdf2f8 100%
            );

        min-height: 100vh;
    }


    /* ================================
    LOGIN CARD
    ================================ */

    .login-card {
        background: rgba(255, 255, 255, 0.92);
        padding: 38px 40px;
        border-radius: 28px;

        box-shadow:
            0 25px 60px rgba(79, 70, 229, 0.18),
            0 8px 25px rgba(15, 23, 42, 0.08);

        border: 1px solid rgba(255, 255, 255, 0.8);

        backdrop-filter: blur(12px);

        margin-top: 35px;
    }


    /* ================================
    LOGO
    ================================ */

    .app-logo {
        width: 82px;
        height: 82px;

        margin: 0 auto 18px auto;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 42px;

        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #7c3aed,
                #ec4899
            );

        border-radius: 24px;

        box-shadow:
            0 12px 30px rgba(99, 102, 241, 0.35);
    }


    /* ================================
    MAIN TITLE
    ================================ */

    .main-title {
        text-align: center;

        font-size: 30px;
        font-weight: 800;

        background:
            linear-gradient(
                90deg,
                #4338ca,
                #7c3aed,
                #db2777
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 8px;
    }


    /* ================================
    SUB TITLE
    ================================ */

    .sub-title {
        text-align: center;

        font-size: 14px;

        color: #64748b;

        line-height: 1.6;

        margin-bottom: 30px;
    }


    /* ================================
    SIGN IN HEADING
    ================================ */

    .signin-header {
        font-size: 23px;

        font-weight: 750;

        color: #111827;

        margin-bottom: 5px;
    }


    /* ================================
    ADMIN MESSAGE
    ================================ */

    .admin-notice {
        font-size: 13px;

        color: #64748b;

        margin-bottom: 20px;
    }


    /* ================================
    INPUT LABELS
    ================================ */

    label {
        color: #374151 !important;

        font-weight: 600 !important;
    }


    /* ================================
    INPUT BOXES
    ================================ */

    div[data-baseweb="input"] {

        background: #f8fafc !important;

        border: 1px solid #dbe4f0 !important;

        border-radius: 12px !important;

        min-height: 48px;

        transition: all 0.2s ease;
    }


    /* Input focus */

    div[data-baseweb="input"]:focus-within {

        background: white !important;

        border-color: #6366f1 !important;

        box-shadow:
            0 0 0 3px rgba(99, 102, 241, 0.12) !important;
    }


    /* Input text */

    div[data-baseweb="input"] input {

        font-size: 14px !important;

        color: #111827 !important;
    }


    /* ================================
    SIGN IN BUTTON
    ================================ */

    div.stFormSubmitButton > button {

        width: 100% !important;

        min-height: 50px !important;

        border: none !important;

        border-radius: 14px !important;

        color: white !important;

        font-size: 16px !important;

        font-weight: 700 !important;

        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #6366f1,
                #7c3aed,
                #db2777
            ) !important;

        box-shadow:
            0 10px 25px rgba(99, 102, 241, 0.30) !important;

        transition: all 0.25s ease !important;
    }


    /* Button hover */

    div.stFormSubmitButton > button:hover {

        transform: translateY(-2px) !important;

        box-shadow:
            0 14px 30px rgba(99, 102, 241, 0.40) !important;

        filter: brightness(1.05);
    }


    /* Button click */

    div.stFormSubmitButton > button:active {

        transform: translateY(0px) !important;
    }


    /* ================================
    WARNING / ERROR
    ================================ */

    div[data-testid="stAlert"] {

        border-radius: 12px !important;

        margin-top: 12px;
    }


    /* ================================
    FOOTER
    ================================ */

    .footer-note {

        text-align: center;

        font-size: 12px;

        color: #94a3b8;

        margin-top: 25px;

        line-height: 1.6;
    }


    /* ================================
    SECURITY TEXT
    ================================ */

    .security {

        text-align: center;

        margin-top: 15px;

        font-size: 12px;

        color: #64748b;
    }


    /* ================================
    SMALL DECORATIVE LINE
    ================================ */

    .login-divider {

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #e2e8f0,
                transparent
            );

        margin: 22px 0;
    }

    </style>
    """, unsafe_allow_html=True)
    # Centered design columns
    col1, col2, col3 = st.columns([1, 1.8, 1])

    with col2:
        st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <div class="app-logo">🚀</div>
                <div class="main-title">Talent Management Platform</div>
                <div class="sub-title">AI powered training & knowledge platform</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="signin-header">Sign in</div>', unsafe_allow_html=True)
            st.markdown('<div class="admin-notice">Use the credentials provided by your administrator.</div>', unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email address", placeholder="example@talentsphere.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                submit = st.form_submit_button("➔ Sign in")
                
                if submit:

                    if not email or not password:

                        st.warning("⚠️ Please fill in all credentials.")

                    else:

                        conn = sqlite3.connect("talent_sphere.db")

                        cursor = conn.cursor()


                        cursor.execute(
                            """
                            SELECT role FROM users
                            WHERE email=? AND password=?
                            """,
                            (email, password)
                        )


                        result = cursor.fetchone()
                        st.write("DATABASE RESULT:", result)  # Debugging line to check the database response


                        conn.close()


                        if result:
                            
                            st.write("Role:", result[0])  # Debugging line to check the role

                            st.session_state["authenticated"] = True

                            st.session_state["user_role"] = result[0]

                            if result[0] == "Admin":
                                st.switch_page("pages/10_Admin.py")
                            else:
                                st.switch_page("pages/1_Dashboard.py")
                                st.rerun()

                        else:

                            st.error(
                                "❌ Invalid email or password"
                            )
            
            st.markdown("""
                <div class="footer-note">
                    🔒 Access is provisioned by your administrator.<br>
                    Contact HR if you have trouble signing in.
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# SCREEN 2: DASHBOARD PAGE (Colorful UI & Sidebar Visible)
# ==========================================
else:
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    # Dashboard CSS
    st.markdown("""
    <style>

    .hero {
        background: linear-gradient(135deg,#6366f1,#8b5cf6);
        padding: 35px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
    }

    .card {
        background: white;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.12);
        text-align: center;
        height: 180px;
    }

    .icon {
        font-size: 45px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin-top: 10px;
    }

    .card-text {
        color:#64748b;
        font-size:14px;
    }

    .section-title {
        font-size:25px;
        font-weight:700;
        margin-top:25px;
    }

    </style>
    """, unsafe_allow_html=True)



    # Sidebar
    if st.session_state["authenticated"]:

        with st.sidebar:

            st.title("🚀 Talent Management Platform")

            # st.write(
            #     f"Welcome, {st.session_state['user_role']}"
            # )

            # st.divider()
            #Common pages (Admin + User)
            st.subheader("workspace")
            
            st.page_link(
                "pages/14_Document.py",
                label="📄 Document"
            )
            st.page_link(
                "pages/6_Semantic_Search.py",
                label="🔍 Search"
            )

        # User Features
            if st.session_state["user_role"] == "User":

                st.page_link(
                    "pages/3_Resume_Analyser.py",
                    label="📄 Resume Analyzer"
                )

                st.page_link(
                    "pages/7_Exams.py",
                    label="📝 Exams"
                )
                st.page_link(
                    "pages/9_User_Chatbot.py",
                    label="🤖 User Assistant"
                )
                st.subheader("Learning portal")
                st.page_link(
                    "pages/16_Learning_portal.py",  
                    label="📚 Learning portal"
                )

        # Admin Features
            else:
                st.subheader("⚙️ Administrator")


                st.write("### Overview")

                st.page_link(
                    "app.py",
                    label="🏠 Dashboard"
                )
                
                st.write("### Administrator")
                st.page_link(
                    "pages/2_AI_Chatbot.py",
                    label="🤖 AI Assistant"
                )


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


            if st.button("Logout 🚪"):

                st.session_state["authenticated"] = False
                st.session_state["user_role"] = None
                st.rerun()


        # Hero Section

        st.markdown(f"""
        <div class="hero">

        <h1>🚀 Talent Management Platform</h1>

        <p>
        Welcome back {st.session_state['user_role']} 👋
        </p>

        <p>
        AI Powered Career Preparation & Knowledge Platform
        </p>

        </div>
        """, unsafe_allow_html=True)



        st.markdown(
            "<div class='section-title'>✨ Explore Features</div>",
            unsafe_allow_html=True
        )


        # Feature Cards

        col1,col2 = st.columns(2)


        with col1:

            st.markdown("""
            <div class="card">

            <div class="icon">🤖</div>

            <div class="card-title">
            AI Chatbot
            </div>

            <div class="card-text">
            Ask questions and get AI powered answers
            </div>

            </div>
            """, unsafe_allow_html=True)



            st.write("")


            st.markdown("""
            <div class="card">

            <div class="icon">📄</div>

            <div class="card-title">
            Resume Analyzer
            </div>

            <div class="card-text">
            Analyze resume and improve skills
            </div>

            </div>
            """, unsafe_allow_html=True)



        with col2:


            st.markdown("""
            <div class="card">

            <div class="icon">📝</div>

            <div class="card-title">
            Mock Exams
            </div>

            <div class="card-text">
            Practice technical and aptitude tests
            </div>

            </div>
            """, unsafe_allow_html=True)



            st.write("")


            st.markdown("""
            <div class="card">

            <div class="icon">🔍</div>

            <div class="card-title">
            Document Search
            </div>

            <div class="card-text">
            Search documents using AI
            </div>

            </div>
            """, unsafe_allow_html=True)



        # Progress Section

        st.markdown(
            "<div class='section-title'>📊 Your Progress</div>",
            unsafe_allow_html=True
        )

        documents,pages,exams=get_dashboard_data()
        c1,c2,c3 = st.columns(3)

        c1.metric(
            "📚 Documents",
            documents
        )

        c2.metric(
            "🤖 AI Sessions",
            pages
        )

        c3.metric(
            "🏆 Tests Completed",
            exams
        )
    # ---------------- ANNOUNCEMENTS ----------------

    import sqlite3


    def get_announcements():

        conn = sqlite3.connect(
            "talent_sphere.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            "SELECT message FROM announcements ORDER BY id DESC"
        )

        data = cursor.fetchall()

        conn.close()

        return data



    st.markdown(
        "<div class='section-title'>📢 Latest Announcements</div>",
        unsafe_allow_html=True
    )


    announcements = get_announcements()


    if announcements:

        for item in announcements:

            st.info(
                f"📢 {item[0]}"
            )

    else:

        st.write(
            "No announcements available."
        )

    st.success(
        "🎉 Platform Status: All systems operational"
    )