import streamlit as st
import os
from populate_database import add_to_chroma as add_to_chroma_pdf, clear_database as clear_database_pdf, load_documents as load_documents_pdf, split_documents as split_documents_pdf
from md import add_to_chroma as add_to_chroma_md, clear_database as clear_database_md, load_documents as load_documents_md, split_documents as split_documents_md
from query_data import query_rag

CHROMA_PATH = "chroma"
DATA_PATH = "data"

# Set up the Streamlit app layout
st.set_page_config(page_title="RAG-based QA", layout="wide")

st.title("RAG-based Question Answering System")

# Sidebar for Database and Document Management
st.sidebar.header("Database Management")
if st.sidebar.button("Reset Database"):
    clear_database_pdf()
    clear_database_md()
    st.sidebar.success("Database has been reset.")

uploaded_files = st.sidebar.file_uploader("Upload documents", type=["txt", "pdf", "md"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(DATA_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.sidebar.success("Files uploaded successfully.")

if st.sidebar.button("Process Documents"):
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

    st.sidebar.success("Documents processed and added to the database.")

# Main content area for interaction
st.header("Ask Questions About Your Documents")

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

query_text = st.text_input("Ask a question about the documents", "")

def query_model(question):
    response = requests.post("https://968f-197-27-65-101.ngrok-free.app/query", json={"question": question})
    if response.status_code == 200:
        return response.json().get("answer")
    else:
        return "Error querying the model."

if st.button("Ask"):
    if query_text:
        response = query_model(query_text)
        st.session_state.conversation.append({
            'question': query_text,
            'answer': response
        })
        st.write(f"**You:** {query_text}")
        st.write(f"**Model:** {response}")

# Display the conversation history
st.subheader("Conversation History")
for interaction in st.session_state.conversation:
    st.write(f"**You:** {interaction['question']}")
    st.write(f"**Model:** {interaction['answer']}")

# Optional: Clear conversation history
if st.button("Clear Conversation"):
    st.session_state['conversation'] = []
