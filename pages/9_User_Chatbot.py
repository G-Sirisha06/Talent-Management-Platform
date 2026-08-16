import streamlit as st
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()
import sqlite3

from src.llm import generate_response
from src.rag import retrieve


st.set_page_config(
    page_title="User AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================
# USER CHECK
# =========================

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None


if not st.session_state["authenticated"]:
    st.warning("Please login first")
    st.stop()


if st.session_state["user_role"] != "User":
    st.error("Access Denied")
    st.stop()



# =========================
# TITLE
# =========================

st.title("🤖 User AI Career Assistant")

st.caption(
    "Ask questions, analyze documents and generate insights using AI"
)



# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("👤 User Menu")


    if st.button("🏠 Dashboard"):

        st.switch_page(
            "pages/1_Dashboard.py"
        )


    st.divider()


    top_k = st.slider(
        "Document Results",
        1,
        10,
        5
    )



# =========================
# DOCUMENT UPLOAD
# =========================

st.subheader("📄 Upload Document")


uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        "Document uploaded successfully"
    )



# =========================
# QUICK ACTIONS
# =========================

st.subheader("⚡ Quick Actions")


c1,c2,c3,c4 = st.columns(4)


with c1:

    if st.button("📄 Summarize"):

        st.session_state.prompt = (
            "Summarize this document"
        )


with c2:

    if st.button("📝 Generate Notes"):

        st.session_state.prompt = (
            "Generate detailed notes from this document"
        )


with c3:

    if st.button("📊 Create Table"):

        st.session_state.prompt = (
            "Create a table from this information"
        )


with c4:

    if st.button("📈 Create Flowchart"):

        st.session_state.prompt = (
            "Create a flowchart for this topic using mermaid format"
        )



# =========================
# CHAT
# =========================


question = st.chat_input(
    "Ask anything..."
)


prompt = question


if "prompt" in st.session_state and not prompt:

    prompt = st.session_state.prompt

    del st.session_state.prompt



if prompt:


    with st.chat_message("user"):

        st.write(prompt)



    with st.chat_message("assistant"):


        with st.spinner("Thinking..."):


            context, sources = retrieve(
                prompt,
                top_k
            )


            final_prompt = f"""

You are Talent Sphere User AI Assistant.

Rules:
- Answer clearly.
- Use document context when available.
- If user asks table, create markdown table.
- If user asks flowchart, create mermaid flowchart.
- If user asks summary, provide structured summary.
- Give simple explanations.

Context:
{context}


Question:
{prompt}

"""


            answer = generate_response(
                final_prompt
            )
            

            conn = sqlite3.connect(
                "talent_sphere.db"
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO chat_history
                (user_email, question, answer)
                VALUES (?, ?, ?)
                """,
                (
                    "User",
                    prompt,
                    answer
                )
            )

            conn.commit()
            conn.close()


            st.write(answer)



            if sources:

                st.markdown(
                    "### 📚 Sources"
                )


                for s in sources:

                    st.write(
                        f"📄 {s['source']} - Page {s['page']}"
                    )