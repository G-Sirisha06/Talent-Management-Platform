import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()

st.set_page_config(page_title="Document Ingestion", page_icon="📥")

st.title("📥 Document Ingestion")

UPLOAD_DIR = "data/uploads"
CHROMA_DIR = "data/chroma_db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

uploaded_files = st.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, file.name)

        with open(file_path, "wb") as f:
            f.write(file.read())

    st.success("✅ Documents Uploaded Successfully")

if st.button("🚀 Build Index"):

    docs = []

    pdfs = os.listdir(UPLOAD_DIR)

    for pdf in pdfs:

        loader = PyPDFLoader(os.path.join(UPLOAD_DIR, pdf))

        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en-v1.5"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    st.success("✅ Index Built Successfully!")

    st.write(f"Total Documents : {len(pdfs)}")
    st.write(f"Total Chunks : {len(chunks)}")