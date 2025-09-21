import streamlit as st
import os
from dotenv import load_dotenv

# Construct the path to the .env file
#dotenv_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..','.env'))

# Load environment variables from .env file
#load_dotenv(dotenv_path=dotenv_path)

# Define the pages
home_page = st.Page("pages/1_home.py", title="Home", icon="🎈")
app_ranking_page = st.Page("pages/2_app_rankings.py", title="App Rankings", icon="❄️")
review_engagement_page = st.Page("pages/3_review_engagement.py", title="Review Engagement", icon="🎉")
competitor_analysis_page = st.Page("pages/4_competitor_analysis.py", title="Competitor Analysis", icon="🎉")

# Set up navigation
pg = st.navigation([home_page,app_ranking_page, review_engagement_page, competitor_analysis_page])

# Run the selected page
pg.run()