import streamlit as st
import os
from utils.database import init_db
from models.chat_logic import handle_user_message
from models.rag_pipeline import load_and_process_pdfs, load_existing_vectorstore

st.set_page_config(
    page_title="AI Doctor Booking Assistant",
    page_icon="🩺",
    layout="wide"
)

init_db()

st.sidebar.title("Navigation")
#page = st.sidebar.radio("Go to", ["Chatbot", "Admin Dashboard"])

# -------- PDF Upload --------
st.sidebar.subheader("📄 Upload PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Upload one or more PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("uploaded_pdfs", exist_ok=True)
    paths = []

    for file in uploaded_files:
        path = f"uploaded_pdfs/{file.name}"
        with open(path, "wb") as f:
            f.write(file.read())
        paths.append(path)

    with st.spinner("Processing PDFs..."):
        st.session_state.vectorstore = load_and_process_pdfs(paths)

    st.sidebar.success("PDFs indexed successfully!")

elif "vectorstore" not in st.session_state:
    st.session_state.vectorstore = load_existing_vectorstore()

# -------- Chatbot --------
if page == "Chatbot":
    st.title("🩺 AI Doctor Appointment Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question or book an appointment")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        response = handle_user_message(user_input, st.session_state)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        with st.chat_message("assistant"):
            st.markdown(response)

#elif page == "Admin Dashboard":
#    import pages.admin_dashboard as admin_dashboard
