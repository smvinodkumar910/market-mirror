import streamlit as st

st.set_page_config(
    page_title="Market Mirror",
    page_icon="👋",
    layout="wide"
)

st.title("Welcome to Market Mirror! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    Market Mirror is an open-source app framework built specifically for
    analyzing the mobile app market.
    
    **👈 Select a page from the sidebar** to see some examples
    of what Market Mirror can do!
"""
)