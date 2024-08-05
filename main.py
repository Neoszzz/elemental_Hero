import streamlit as st
import os
from populate_database import add_to_chroma as add_to_chroma_pdf, clear_database as clear_database_pdf, load_documents as load_documents_pdf, split_documents as split_documents_pdf
from md import add_to_chroma as add_to_chroma_md, clear_database as clear_database_md, load_documents as load_documents_md, split_documents as split_documents_md
from query_data import query_rag

CHROMA_PATH = "chroma"
DATA_PATH = "data"

st.title("RAG-based Question Answering")

# Clear the database if needed
if st.button("Reset Database"):
    clear_database_pdf()
    clear_database_md()
    st.success("Database has been reset.")

# Upload documents
uploaded_files = st.file_uploader("Upload documents", type=["txt", "pdf", "md"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(DATA_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("Files uploaded successfully.")

# Process documents
if st.button("Process Documents"):
    pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.pdf')]
    md_txt_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.md') or f.endswith('.txt')]

    if pdf_files:
        documents_pdf = load_documents_pdf()
        chunks_pdf = split_documents_pdf(documents_pdf)
        add_to_chroma_pdf(chunks_pdf)
    
    if md_txt_files:
        documents_md = load_documents_md()
        chunks_md = split_documents_md(documents_md)
        add_to_chroma_md(chunks_md)

    st.success("Documents processed and added to the database.")

# Query the database
query_text = st.text_input("Ask a question about the documents")
if query_text:
    response = query_rag(query_text)
    st.write(f"Answer: {response}")
