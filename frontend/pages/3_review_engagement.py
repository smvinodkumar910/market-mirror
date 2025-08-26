import streamlit as st
import pandas as pd

from tools.read_data import  get_app_list_for_prompt, get_review_data
st.set_page_config(layout="wide")

st.sidebar.header("App Reviews")
st.title("Review Engagement")


get_app_list_for_prompt = get_app_list_for_prompt()

genre = st.sidebar.selectbox(label='Select App Category', options=get_app_list_for_prompt['app_genre'].unique().tolist())

app_name = st.sidebar.selectbox(label='Select App Name', options=get_app_list_for_prompt[get_app_list_for_prompt['app_genre']==genre]['app_name'].unique().tolist())

review_sentiment = st.sidebar.selectbox(label='Select Review Sentiment', options=['Positive','Neutral','Negative'])

df = get_review_data(genre, app_name, review_sentiment)

st.dataframe(df, use_container_width=True, hide_index=True)
