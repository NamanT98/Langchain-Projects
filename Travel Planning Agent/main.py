from helper import *
import streamlit as st
import datetime

st.title("Travel Planning Agent")
if "chatbot" not in st.session_state:
    st.session_state.chatbot = TravelAgent()
    st.session_state.chatbot.get_agent()

if "submit" not in st.session_state:
    st.session_state.submit = False


startdate = st.date_input(
    "Start Date", min_value=datetime.date.today(), format="YYYY-MM-DD"
)
enddate = st.date_input("End Date", min_value=startdate, format="YYYY-MM-DD")

destination = st.text_input("Destination")

source = st.text_input("Source")


if st.button("Plan a trip") and startdate and enddate:
    st.session_state.submit = True
    with st.spinner("Planning your trip..."):
        query = f"Plan a trip between {startdate} and {enddate} from source Raipur to destination {destination}."
        results = st.session_state.chatbot.run_agent(query)
        st.markdown(results)
