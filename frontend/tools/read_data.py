from google.cloud import bigquery
import streamlit as st

@st.cache_data
def get_review_summary():
    # Construct a BigQuery client object.
    client = bigquery.Client()

    query = """
    SELECT 
    s.app_genre
    , app_dtl.app_name
    , app_dtl.app_rank
    , app_dtl.total_reviews
    , app_dtl.sentiment_proportion_positive
    , app_dtl.sentiment_proportion_neutral
    , app_dtl.sentiment_proportion_negative
    FROM 
    `market-mirror-dev.APP_MARKET_GOLD.T_APP_REVIEWS_GENRE_LEVEL_SUMMARY` s,
    unnest(s.app_dtl) as app_dtl
    """
    query_job = client.query(query)  # Make an API request.

    query_job.result()  # Wait for the job to complete.

    df = query_job.to_dataframe()

    return df


@st.cache_data
def get_app_list_for_prompt():
    client = bigquery.Client()

    query = f"""
    SELECT distinct
    a.app_genre,
    a.app_name
    FROM
    `market-mirror-dev.APP_MARKET_GOLD.T_APP_REVIEWS_DETAIL` a;
    """
    query_job = client.query(query)  # Make an API request.

    query_job.result()  # Wait for the job to complete.

    df = query_job.to_dataframe()

    return df

@st.cache_data
def get_google_apps_list():
    client = bigquery.Client()

    query = f"""
    select 
    distinct 
    a.app_name, 
    a.app_description ,
    a.app_genre
    from `market-mirror-dev.APP_MARKET_GOLD.T_GOOGLE_APP_DETAIL_FINAL` a;
    """
    query_job = client.query(query)  # Make an API request.

    query_job.result()  # Wait for the job to complete.

    df = query_job.to_dataframe()

    return df



@st.cache_data
def get_review_data(genre:str, app_name:str, review_sentiment:str):
    
    client = bigquery.Client()

    genre_filter =  f"AND a.app_genre='{genre}' "  if len(genre)>0 else ''
    app_name_filter =  f"AND a.app_name='{app_name}' "  if len(app_name)>0 else ''
    sentiment_filter =  f"AND a.sentiment='{review_sentiment}' "  if len(review_sentiment)>0 else ''  


    query = f"""
    SELECT
    r.id,
    r.review_text,
    r.review_response,
    case when r.review_response='' then False else True end as generate_response
    FROM
    `market-mirror-dev.APP_MARKET_GOLD.T_APP_REVIEWS_DETAIL` a,
    UNNEST(a.review_data) AS r
    WHERE 1=1
    {genre_filter}
    {app_name_filter}
    {sentiment_filter}
    """
    query_job = client.query(query)  # Make an API request.

    query_job.result()  # Wait for the job to complete.

    df = query_job.to_dataframe()

    return df
    
