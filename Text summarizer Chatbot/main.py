from helper import *
import streamlit as st

st.title("Text Summarizer")
if 'submit' not in st.session_state:
    st.session_state.submit=False
if 'chatbot' not in st.session_state:
    st.session_state.chatbot=TextSummarizer()

st.markdown("Paste Text here...")
text= st.text_area(label='text area',height=400,label_visibility='hidden')

if text:
    response=st.session_state.chatbot.run_chain(text)
    st.markdown("Summarized Text")
    st.write("\n"+response)