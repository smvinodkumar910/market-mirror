
create or replace table `market-mirror-dev.APP_MARKET_GOLD.T_APP_REVIEWS_AGG`
AS
select 
app_name
, app_genre
, total_reviews
, ifnull(sentiment_count_positive,0) as sentiment_count_positive
, ifnull(sentiment_prop_Positive,0) as sentiment_proportion_positive
, ifnull(sentiment_count_neutral,0) as sentiment_count_neutral
, ifnull(sentiment_prop_neutral,0) as sentiment_proportion_neutral
, ifnull(sentiment_count_negative,0) as sentiment_count_negative
, ifnull(sentiment_prop_negative,0) as sentiment_proportion_negative
, dense_rank() over(partition by app_genre order by total_reviews desc, ifnull(sentiment_prop_Positive,0) desc, ifnull(sentiment_prop_negative,0) desc, ifnull(sentiment_prop_negative,0) desc) as app_rank
from
(select app_name, app_genre, sentiment, sentiment_count, total_reviews, round((sentiment_count/total_reviews)*100,2) sentiment_proportion
from
(select  app_name, app_genre, sentiment, count(1) OVER(PARTITION BY app_name, app_genre, sentiment) sentiment_count, count(1) OVER(PARTITION BY app_name) total_reviews
  from `market-mirror-dev.APP_MARKET_SILVER.T_APP_REVIEWS_CLEANED`
)
group by app_name, app_genre, sentiment, sentiment_count, total_reviews
)
pivot (SUM(sentiment_count) as sentiment_count, SUM(sentiment_proportion) as sentiment_prop FOR sentiment in ('Positive','Neutral','Negative'));

create or replace table `market-mirror-dev.APP_MARKET_GOLD.T_APP_REVIEWS_GENRE_LEVEL_SUMMARY`
AS
select 
app_genre
, array_agg(
  struct(
  app_name
  ,app_rank
  ,total_reviews
  ,sentiment_count_positive
  ,sentiment_proportion_positive
  ,sentiment_count_neutral
  ,sentiment_proportion_neutral
  ,sentiment_count_negative
  ,sentiment_proportion_negative
  )) as app_dtl from `market-mirror-dev.APP_MARKET_GOLD.T_APP_REVIEWS_AGG`
group by app_genre;
--where app_rank <= 15


create or replace table `market-mirror-dev.APP_MARKET_GOLD.T_APP_REVIEWS_DETAIL`
AS
select r.app_genre, r.app_name, r.sentiment, ARRAY_AGG(r.review_text) review_text from `market-mirror-dev.APP_MARKET_SILVER.T_APP_REVIEWS_CLEANED` r
group by r.app_genre, r.app_name, r.sentiment;
