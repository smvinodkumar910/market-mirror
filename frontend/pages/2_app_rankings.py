import streamlit as st
import pandas as pd
import plotly.express as px
from tools.read_data import get_review_summary

st.sidebar.header("App Reviews")
st.title("App Rankings by Category")

df = get_review_summary()

categories_list = df['app_genre'].unique().tolist()

category = st.sidebar.selectbox(label='Select App Category', options=categories_list)

st.subheader(f"Ranking for {category}")

filtered_df = df[(df.app_genre==category) & (df.app_rank<=10)][['app_name','app_rank','total_reviews','sentiment_proportion_positive','sentiment_proportion_neutral','sentiment_proportion_negative']].sort_values(by='app_rank',ascending=True)
filtered_df.rename(columns={'sentiment_proportion_positive':'Positive','sentiment_proportion_neutral':'Neutral','sentiment_proportion_negative':'Negative'},inplace=True)


# Create the plot with plotly express
fig = px.bar(
    filtered_df, 
    x=['Positive', 'Neutral', 'Negative'], 
    y='app_name',
    text=filtered_df['total_reviews'],
    orientation='h',
    title=f"Sentiment Analysis for {category} Apps",
    labels={'value': '% of sentiment of reviews', 'variable': 'Sentiment'},
    height=600, # You can adjust this value to fit your labels
    category_orders={'variable': ['Positive', 'Neutral', 'Negative']}
)

# Update layout for better readability
fig.update_layout(
    yaxis_title='App Name',
    xaxis_title='% of sentiment of reviews',
    legend_title='Sentiment',
    yaxis={'categoryorder':'array', 'categoryarray': filtered_df['app_name'].tolist()[::-1]},
    uniformtext_minsize=8, 
    uniformtext_mode='hide'
)

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(filtered_df)