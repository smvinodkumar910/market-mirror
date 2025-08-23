import streamlit as st
import pandas as pd
import plotly.express as px
from tools.read_data import get_review_summary

st.sidebar.header("App Reviews")

df = get_review_summary()

categories_list = df['app_genre'].unique().tolist()

category = st.sidebar.selectbox(label='Select App Category', options=categories_list)

top_apps =st.sidebar.slider(label="Top Apps", min_value=1, max_value=10, value=10, step=1)

st.subheader(f"Ranking for {category}")

filtered_df = df[(df.app_genre==category) & (df.app_rank<=top_apps)][['app_name','app_rank','total_reviews','sentiment_proportion_positive','sentiment_proportion_neutral','sentiment_proportion_negative']]
filtered_df.rename(columns={'sentiment_proportion_positive':'Positive','sentiment_proportion_neutral':'Neutral','sentiment_proportion_negative':'Negative'},inplace=True)
filtered_df = filtered_df.sort_values(by=['Positive','Neutral','Negative'],ascending=[False,False,False])



# Create the plot with plotly express
fig = px.bar(
    filtered_df, 
    x=['Positive', 'Neutral', 'Negative'], 
    y='app_name',
    orientation='h',
    title=f"Sentiment Analysis for {category} Apps",
    height=600, # You can adjust this value to fit your labels
    category_orders={'variable': ['Positive', 'Neutral', 'Negative']},
    labels={'variable': 'Sentiment', 'app_name': 'App Name', 'value': '% of sentiment of reviews'},
    # color_discrete_map={'Positive': "#4DA44D",  # A shade of green 
    #                     'Neutral': 'lightgrey',
    #                     'Negative': "#b96464"   # A shade of red
    #                     }        
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

st.subheader("Raw Data")
st.dataframe(filtered_df)