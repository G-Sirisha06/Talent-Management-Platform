from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5"
)

db = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings
)

def retrieve(query, k=5):

    results = db.similarity_search_with_score(query, k=k)

    context = ""
    sources = []

    for doc, score in results:
        if score >1.2:
            continue
        context += doc.page_content + "\n\n"
        sources.append({
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", "N/A")
        })
    return context, sources
        