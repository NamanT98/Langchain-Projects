from helper import *
import streamlit as st

st.title("Motivational Speaker Chatbot")

if 'chatbot' not in st.session_state:
    st.session_state.chatbot=MotivationalSpeaker()
if 'messages' not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input= st.chat_input("You can talk about your problems here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role":"user","content":user_input})
    response=st.session_state.chatbot.run_chain(user_input)
    st.session_state.messages.append({"role":"assistant","content":response})
    st.chat_message("assistant").markdown(response)