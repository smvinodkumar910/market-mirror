import streamlit as st

import streamlit as st

# Define the pages
home_page = st.Page("pages/1_home.py", title="Home", icon="🎈")
app_ranking_page = st.Page("pages/2_app_rankings.py", title="App Rankings", icon="❄️")
review_engagement_page = st.Page("pages/3_review_engagement.py", title="Review Engagement", icon="🎉")
competitor_analysis_page = st.Page("pages/4_competitor_analysis.py", title="Competitor Analysis", icon="🎉")

# Set up navigation
pg = st.navigation([home_page,app_ranking_page, review_engagement_page, competitor_analysis_page])

# Run the selected page
pg.run()