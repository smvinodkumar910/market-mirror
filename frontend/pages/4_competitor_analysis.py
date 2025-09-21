import streamlit as st
from tools.read_data import  get_google_apps_list
from tools.app_analysis_wf import get_competitor_summary

st.set_page_config(layout="wide")
st.sidebar.header("Analyze")
st.header("Competitor Analysis by Gemini")




get_app_list_for_prompt = get_google_apps_list()

genre = st.sidebar.selectbox(label='Select App Category', options=get_app_list_for_prompt['app_genre'].unique().tolist())

app_name = st.sidebar.selectbox(label='Select App Name', options=get_app_list_for_prompt[get_app_list_for_prompt['app_genre']==genre]['app_name'].unique().tolist())

if st.sidebar.button("Analyze"):
    with st.spinner("Analyzing..."):
        llm_feedback = get_competitor_summary(app_name)
        st.markdown(llm_feedback)
else:
    st.success("This page performs a competitive analysis. The user selects an app, and the tool finds similar apps on other platforms and provides a comparison, including advantages, disadvantages, and an improvement plan.")