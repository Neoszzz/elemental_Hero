import streamlit as st
import os
import subprocess
from populate_database import add_to_chroma as add_to_chroma_pdf, load_documents as load_documents_pdf, split_documents as split_documents_pdf
from md import add_to_chroma as add_to_chroma_md, load_documents as load_documents_md, split_documents as split_documents_md
from query_data import query_rag  # Import query_rag from query_data

CHROMA_PATH = "chroma"
DATA_PATH = "data"

# Function to reset the database by calling populate_database with --reset
def clear_database():
    subprocess.run(["python", "populate_database.py", "--reset"])
    subprocess.run(["python", "md.py", "--reset"])

# Set up the Streamlit app layout
st.set_page_config(page_title="RAG-based QA", layout="centered")

st.title("Elemental Hero Assistant - Neos")

# Sidebar for Database and Document Management
with st.sidebar:
    st.header("Database Management")
    if st.button("Reset Database"):
        clear_database()
        st.success("Database has been reset.")
    
    uploaded_files = st.file_uploader("Upload documents", type=["txt", "pdf", "md"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(DATA_PATH, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success("Files uploaded successfully.")
    
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

# Main content area for interaction
st.header("Ask Questions About Your Documents")

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

query_text = st.text_input("Ask a question about the documents", "")

if st.button("Ask"):
    if query_text:
        response = query_rag(query_text)
        if response:
            st.session_state.conversation.append({
                'question': query_text,
                'answer': response
            })
            st.markdown(f"**You:** {query_text}")
            st.markdown(f"**Neos:** {response}")
        else:
            st.markdown("**Neos:** No response received from the assistant.")

# Display the conversation history
st.subheader("Conversation History")
for interaction in st.session_state.conversation:
    st.markdown(f"**You:** {interaction['question']}")
    st.markdown(f"**Neos:** {interaction['answer']}")

# Optional: Clear conversation history
if st.button("Clear Conversation"):
    st.session_state['conversation'] = []
    st.experimental_rerun()
