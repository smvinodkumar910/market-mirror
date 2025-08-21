import streamlit as st
import pandas as pd
from tools.read_data import get_review_summary

st.sidebar.header("App Reviews")
st.title("App Rankings by Category")

df = get_review_summary()

categories_list = df['app_genre'].unique().tolist()

category = st.selectbox(label='Select App Category', options=categories_list)

st.subheader(f"Ranking for {category}")

# Placeholder for visualization
st.bar_chart(df[df['app_genre'] == category]['app_rank'].value_counts())

st.subheader("Raw Data")
st.dataframe(df[df['app_genre'] == category])
