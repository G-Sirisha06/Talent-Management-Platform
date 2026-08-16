import streamlit as st
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️"
)


st.title("⚙️ System Settings")


st.subheader("🔧 Platform Configuration")


app_name = st.text_input(
    "Application Name",
    "Talent Sphere Elevate"
)


mode = st.selectbox(
    "Platform Mode",
    [
        "Production",
        "Development"
    ]
)


notifications = st.checkbox(
    "Enable Notifications",
    value=True
)


if st.button("💾 Save Settings"):

    st.success(
        "✅ Settings saved successfully"
    )


st.divider()


st.subheader("🔐 Security")

st.write(
    "✔ User authentication enabled"
)

st.write(
    "✔ Role based access control enabled"
)