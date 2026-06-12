import streamlit as st

from features.insurance_dictionary.page import render


st.set_page_config(
    page_title="AI 보험용어사전",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

render()
