import streamlit as st
from helper import *

st.title("LangChain")
user_input=st.text_input("Ask questions about pdf")

if 'submit' not in st.session_state:
    st.session_state.submit=False

with st.sidebar:
# if not st.session_state.file:
    pdf_docs=st.file_uploader("Upload your pdf files !",accept_multiple_files=True)
    if st.button("Submit"):
        st.session_state.submit=True
        with st.spinner("Processing..."):
            st.session_state.db=load_document(pdf_docs)
            st.session_state.new_chain=get_qa_chain()
            st.success("Done")

if not st.session_state.submit:
    st.write("Please upload your pdf files")

if user_input and st.session_state.submit:
    response=run_qa(user_input,st.session_state.db,st.session_state.new_chain)
    st.write(response)