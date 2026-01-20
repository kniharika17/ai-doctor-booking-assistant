import streamlit as st
from models.chat_logic import handle_user_message

st.set_page_config(page_title="AI Doctor Booking Assistant", page_icon="🩺")

st.title("🩺 AI Doctor Appointment Assistant")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask a question or book an appointment")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    response = handle_user_message(user_input, st.session_state.messages)

    # Store bot message
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
