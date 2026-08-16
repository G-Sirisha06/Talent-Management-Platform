import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()

st.set_page_config(
    page_title="Semantic Search",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Semantic Search")

CHROMA_DIR = "data/chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5"
)

db = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

query = st.text_input("Enter your question")
k=st.slider("Number of Results", min_value=1, max_value=10, value=5)
if st.button("Search"):

    if query.strip() == "":
        st.warning("Please enter a question.")
    else:

        results = db.similarity_search_with_score(query, k=k)

        st.success(f"Top {len(results)} Results")

        for i, (doc, score) in enumerate(results, start=1):

            st.markdown(f"### 📄 Result {i}")

            st.write("**Source:**", doc.metadata.get("source", "Unknown"))

            st.write("**Page:**", doc.metadata.get("page", "N/A"))

            st.write("**Similarity Score:**", round(score, 4))

            st.write(doc.page_content)

            st.divider()