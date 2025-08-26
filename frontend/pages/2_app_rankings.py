import streamlit as st
import pandas as pd
import plotly.express as px
from tools.read_data import get_review_summary
from tools.generate_summary import generate_summary


st.set_page_config(layout="wide")

st.sidebar.header("App Reviews")

container = st.container(border=True)


df = get_review_summary()

categories_list = df['app_genre'].unique().tolist()

category = st.sidebar.selectbox(label='Select App Category', options=categories_list)

top_apps =st.sidebar.slider(label="Top Apps", min_value=1, max_value=10, value=10, step=1)

st.subheader(f"Ranking for {category}")

filtered_df = df[df.app_genre==category][['app_name','app_rank','total_reviews','sentiment_proportion_positive','sentiment_proportion_neutral','sentiment_proportion_negative']]
filtered_df.rename(columns={'sentiment_proportion_positive':'Positive','sentiment_proportion_neutral':'Neutral','sentiment_proportion_negative':'Negative'},inplace=True)
filtered_df = filtered_df.sort_values(by=['Positive','Neutral','Negative'],ascending=[False,False,False])
filtered_df = filtered_df.head(top_apps)
summary_text = generate_summary(filtered_df)
container.write(summary_text)



# Create the plot with plotly express
fig = px.bar(
    filtered_df, 
    x=['Positive', 'Neutral', 'Negative'], 
    y='app_name',
    orientation='h',
    title=f"Sentiment Analysis for {category} Apps",
    height=600, # You can adjust this value to fit your labels
    category_orders={'variable': ['Positive', 'Neutral', 'Negative']},
    labels={'variable': 'Sentiment', 'app_name': 'App Name', 'value': '% of sentiment of reviews'}       
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

st.plotly_chart(fig, use_container_width=True)

st.subheader("Number of Reviews")

review_cnt = filtered_df[['app_name','total_reviews']].sort_values(by='total_reviews',ascending=False)


# Create the plot with plotly express
fig2 = px.bar(
    review_cnt, 
    x='app_name', 
    y='total_reviews',
    orientation='v',
    title=f"Number of Reviews for {category} Apps",
    height=600, # You can adjust this value to fit your labels
) 
    
st.plotly_chart(fig2, use_container_width=True)