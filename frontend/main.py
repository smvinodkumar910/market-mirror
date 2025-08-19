"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from read_data import get_review_data

df = get_review_data()

categories_list = df['app_genre'].unique().tolist()

st.selectbox(label='App Category',options=categories_list)

st.write(df)
