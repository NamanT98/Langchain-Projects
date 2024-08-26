from helper import *
import streamlit as st

st.title("Language Translation")
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Translator()

with st.sidebar:
    lang1 = st.text_input("Source language")
    lang2 = st.text_input("Target language")

st.markdown("Paste Text here...")
text = st.text_area(label="text area", height=400, label_visibility="hidden")

if text and lang1 and lang2:
    response = st.session_state.chatbot.run_chain(text, (lang1, lang2))
    st.write("\n" + response)
