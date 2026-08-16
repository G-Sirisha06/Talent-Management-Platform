import streamlit as st
import os
from pypdf import PdfReader
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from src.sidebar import hide_Pages_sidebar
hide_Pages_sidebar()


st.set_page_config(
    page_title="Documents",
    page_icon="📄",
    layout="wide"
)


st.title("📄 Documents Library")


UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "data",
    "uploads"
)

total_documents = 0
total_pages = 0
files = []


# ==============================
# FETCH DOCUMENTS
# ==============================

if os.path.exists(UPLOAD_DIR):

    files = [
        file for file in os.listdir(UPLOAD_DIR)
        if file.endswith(".pdf")
    ]


    total_documents = len(files)


    for file in files:

        path = os.path.join(
            UPLOAD_DIR,
            file
        )

        reader = PdfReader(path)

        total_pages += len(reader.pages)



# ==============================
# REAL CHUNKS FROM CHROMA
# ==============================

total_chunks = 0

chroma_path = os.path.join(
    BASE_DIR,
    "data",
    "chroma"
)


if os.path.exists(chroma_path):

    try:

        import chromadb

        client = chromadb.PersistentClient(
            path=chroma_path
        )


        collections = client.list_collections()


        if collections:

            collection = client.get_collection(
                collections[0].name
            )


            total_chunks = collection.count()


    except Exception:

        total_chunks = 0



# ==============================
# METRICS
# ==============================


col1, col2, col3 = st.columns(3)


col1.metric(
    "📚 Total Documents",
    total_documents
)


col2.metric(
    "📑 Total Pages",
    total_pages
)


col3.metric(
    "🧩 Total Chunks",
    total_chunks
)



st.divider()



# ==============================
# LIBRARY PREVIEW
# ==============================


st.subheader(
    "📦 Library Preview"
)


if files:

    for file in files:

        st.success(
            f"📄 {file}"
        )


else:

    st.warning(
        "No documents available"
    )