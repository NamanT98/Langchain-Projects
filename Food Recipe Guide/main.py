from helper import *
import streamlit as st
import datetime

st.set_page_config(layout="wide")
st.title("Master Chef")
if "chatbot" not in st.session_state:
    st.session_state.chatbot = FoodRecipeAgent()
    st.session_state.chatbot.get_agent()

if "submit" not in st.session_state:
    st.session_state.submit = False

item_name = st.text_input("Food Item Name")


if st.button("Get Recipe") and item_name:
    st.session_state.submit = True
    with st.spinner("Cooking your recipe..."):
        results = st.session_state.chatbot.run_agent(item_name)
        st.markdown(results)
