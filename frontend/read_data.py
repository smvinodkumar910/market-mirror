from google.cloud import bigquery


def get_review_data():
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
