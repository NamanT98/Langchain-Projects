import streamlit as st
from helper import *

st.title("PDF QA Chatbot")
if "submit" not in st.session_state:
    st.session_state.submit = False
if "chatbot" not in st.session_state:
    st.session_state.chatbot = PdfChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask questions about Youtube Video")

with st.sidebar:
    pdf_docs = st.file_uploader("Upload your pdf files !", accept_multiple_files=True)
    if st.button("Submit"):
        st.session_state.submit = True
        with st.spinner("Processing..."):
            st.session_state.chatbot.create_db(pdf_docs)
            st.success("Done")

if not st.session_state.submit:
    st.write("Please upload your pdf files")

if user_input and st.session_state.submit:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = st.session_state.chatbot.run_chain(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").markdown(response)
