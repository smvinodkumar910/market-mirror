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

    ### What's inside?

    - **App Rankings:** This page displays app rankings within a selected category. It shows a bar chart of sentiment analysis (Positive, Neutral, Negative) for the top apps and another bar chart for the number of reviews. It also provides a summary of the rankings.

    - **Review Engagement:** This page allows users to view and engage with app reviews. Users can filter reviews by app category, app name, and sentiment. They can then select reviews and generate a response using a language model.

    - **Competitor Analysis:** This page performs a competitive analysis. The user selects an app, and the tool finds similar apps on other platforms and provides a comparison, including advantages, disadvantages, and an improvement plan.
"""
)