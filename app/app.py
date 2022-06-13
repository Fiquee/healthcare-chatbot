import streamlit as st
import app_admin
import app_chatbot

st.set_page_config(page_title="Patient Satisfaction Monitoring BOT")

pages = {
    "Chatbot": app_chatbot,
    "Admin": app_admin
}

st.header("Patient Satisfaction Monitoring BOT")
st.sidebar.header("Navigation")
selection = st.sidebar.selectbox("Select page:", options=list(pages.keys()))

page = pages[selection]
page.app()
