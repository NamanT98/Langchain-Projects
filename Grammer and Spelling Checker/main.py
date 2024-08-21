from helper import *
import streamlit as st

st.title("Grammer and Spelling Checker")

if 'chatbot' not in st.session_state:
    st.session_state.chatbot=TextSummarizer()

st.markdown("Paste Text here...")
text= st.text_area(label='text area',height=400,label_visibility='hidden')

if text:
    response=st.session_state.chatbot.run_chain(text)
    if "Everything is correct" in response:
        st.markdown("Corrected Text")
    st.write("\n"+response)