from helper import *
import streamlit as st

st.title("Marketing Email Generator")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = EmailGenerator()

st.markdown("Write a detailed product description here...")
text = st.text_area(label="text area", height=400, label_visibility="hidden")

if text:
    response = st.session_state.chatbot.run_chain(text)
    st.write("\n" + response)
