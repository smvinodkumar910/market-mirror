import streamlit as st
import pandas as pd
from streamlit_card import card

from tools.read_data import  get_app_list_for_prompt, get_review_data
from tools.genai_tools import generate_review_response
st.set_page_config(layout="wide")

st.sidebar.header("App Reviews")
st.title("Review Engagement")

get_app_list_for_prompt = get_app_list_for_prompt()

genre = st.sidebar.selectbox(label='Select App Category', options=get_app_list_for_prompt['app_genre'].unique().tolist())

app_name = st.sidebar.selectbox(label='Select App Name', options=get_app_list_for_prompt[get_app_list_for_prompt['app_genre']==genre]['app_name'].unique().tolist())

review_sentiment = st.sidebar.selectbox(label='Select Review Sentiment', options=['Positive','Neutral','Negative'])

df = get_review_data(genre, app_name, review_sentiment)


if df.shape[0] > 0:
    # Create a unique key for the session state based on filters
    session_key_filters = f"filters_{genre}_{app_name}_{review_sentiment}"
    session_key_df = "review_df"

    # If filters have changed, reset the dataframe in session state
    if st.session_state.get('current_filters') != session_key_filters:
        st.session_state.current_filters = session_key_filters
        df['generate_response'] = False
        # The 'review_response' from DB should be preserved.
        st.session_state[session_key_df] = df.copy()
    elif session_key_df not in st.session_state:
        st.session_state[session_key_df] = df.copy()


    edited_df = st.data_editor(
        st.session_state[session_key_df],
        hide_index=True,
        use_container_width=True,
        column_config={
            "generate_response": st.column_config.CheckboxColumn(
                "Generate Response",
                default=False,
            ),
            "review_text": st.column_config.TextColumn("Review"),
            "review_response": st.column_config.TextColumn("Generated Response"),
        },
        disabled=["id", "review_text", "review_response"],
        key="review_editor"
    )

    # Find rows where 'generate_response' is newly checked
    newly_checked_mask = (edited_df['generate_response']) & (edited_df['review_response'] == '')
    
    if newly_checked_mask.any():
        for index in edited_df[newly_checked_mask].index:
            with st.spinner(f"Generating response for review..."):
                review_text = edited_df.loc[index, 'review_text']
                response = generate_review_response(app_name=app_name, genre=genre, review_text=review_text, language='English')
                edited_df.loc[index, 'review_response'] = response
                edited_df.loc[index, 'generate_response'] = True
        
        # Update the dataframe in session state
        st.session_state[session_key_df] = edited_df
        # Rerun to show the updated responses and clear the spinner
        st.rerun()

else:
    st.text('No reviews found')
    if "review_df" in st.session_state:
        del st.session_state["review_df"]
    
