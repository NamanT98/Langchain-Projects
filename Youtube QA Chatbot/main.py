from helper import *
import streamlit as st

st.title("Youtube video QA Chatbot")
if "submit" not in st.session_state:
    st.session_state.submit = False
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBot()
if "messages" not in st.session_state:
    st.session_state.messages = []

# st.session_state.messages.append({"role":"assistant","content":"Hello👋 I am a Youtube video Question Answering bot. To start, paste the youtube video link and press submit"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask questions about Youtube Video")

with st.sidebar:
    url = st.text_input("Upload Youtube URL !")
    if st.button("Submit"):
        st.session_state.submit = True
        with st.spinner("Processing..."):
            st.session_state.chatbot.create_db(url)
            st.success("Done")

if not st.session_state.submit:
    st.write("Please upload URL !")

if user_input and st.session_state.submit:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = st.session_state.chatbot.run_chain(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").markdown(response)
