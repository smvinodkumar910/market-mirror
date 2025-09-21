from google.genai import Client, types
import pandas as pd
import streamlit as st

@st.cache_data
def generate_summary(df: pd.DataFrame):
    df_data = df.to_json(orient='records')
    client = Client(vertexai=True,project='market-mirror-dev', location='us-central1')

    sys_instruction = types.GenerateContentConfig(system_instruction="You are a professional Data Analyst. When you are provided with some " \
    "data in JSON format you have to provide a summary of the data. You will be provided with android app review data with sentiment details." \
    "Inclulding how many Positive / Neutral / Negative reviews each app got. You have to provide a short summary in less than 10 lines of the data provided.")
    
    prompt = ['please provide summary for the app review data here : ' + df_data + '']
        
    response = client.models.generate_content(model="gemini-2.5-flash" ,contents=prompt, config=sys_instruction)

    return response.text


@st.cache_data
def generate_review_response(app_name: str, genre: str,review_text: str, language:str):
    
    client = Client(vertexai=True,project='market-mirror-dev', location='us-central1')

    sys_instruction = types.GenerateContentConfig(system_instruction="You are a professional Customer Engagement Officer." \
                                                  "You will be handling Customers and reply to them politely for their reviews in the on the app."\
                                                  "You will be replying to the customers in their own language as required."\
                                                  "You will provide your answer in less than 6 lines",
                                                  temperature=0.5)
    
    prompt = ['please provide reponse to the customer in the language ' + language + ' for their review for the app '+ app_name + 'belongs to the genre '+ genre, 'review_text : '+review_text ]
        
    response = client.models.generate_content(model="gemini-2.5-flash" ,contents=prompt, config=sys_instruction)

    return response.text
