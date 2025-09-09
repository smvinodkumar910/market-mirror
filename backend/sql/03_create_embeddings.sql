CREATE OR REPLACE TABLE `market-mirror-dev.APP_MARKET_GOLD.T_WINDOWS_APP_DESC_EMBEDDED` AS
SELECT 
app_name as content, ml_generate_embedding_result as embedding, ml_generate_embedding_statistics, ml_generate_embedding_status
FROM ML.GENERATE_EMBEDDING(
    MODEL `market-mirror-dev.APP_MARKET_SILVER.embeddings`,
    (SELECT app_name, app_description AS content FROM `market-mirror-dev.APP_MARKET_SILVER.T_WINDOWS_APP_DETAIL_CLEANED`
    ---where app_name='Super leps Jabber jump world'
    ),
    struct(
      True as flatten_json_output,
      'SEMANTIC_SIMILARITY' as task_type
    )
);

CREATE OR REPLACE TABLE `market-mirror-dev.APP_MARKET_GOLD.T_APPLE_APP_DESC_EMBEDDED` AS
SELECT 
app_name as content, ml_generate_embedding_result as embedding, ml_generate_embedding_statistics, ml_generate_embedding_status
FROM ML.GENERATE_EMBEDDING(
    MODEL `market-mirror-dev.APP_MARKET_SILVER.embeddings`,
    (SELECT app_name, app_description AS content FROM `market-mirror-dev.APP_MARKET_SILVER.T_APPLE_APP_DETAIL_CLEANED`
    ---where app_name='Super leps Jabber jump world'
    ),
    struct(
      True as flatten_json_output,
      'SEMANTIC_SIMILARITY' as task_type
    )
);



CREATE OR REPLACE TABLE `market-mirror-dev.APP_MARKET_GOLD.T_GOOGLE_APP_DESC_EMBEDDED` AS
SELECT 
app_name as content, ml_generate_embedding_result as embedding, ml_generate_embedding_statistics, ml_generate_embedding_status
FROM ML.GENERATE_EMBEDDING(
    MODEL `market-mirror-dev.APP_MARKET_SILVER.embeddings`,
    (SELECT app_name, app_description AS content FROM `market-mirror-dev.APP_MARKET_SILVER.T_GOOGLE_APP_DETAIL_CLEANED`
    ---where app_name='Super leps Jabber jump world'
    ),
    struct(
      True as flatten_json_output,
      'SEMANTIC_SIMILARITY' as task_type
    )
);


DROP VECTOR INDEX `APPLE_VECTOR_INDEX` ON `market-mirror-dev.APP_MARKET_GOLD.T_APPLE_APP_DESC_EMBEDDED`;
DROP VECTOR INDEX `GOOGLE_VECTOR_INDEX` ON `market-mirror-dev.APP_MARKET_GOLD.T_GOOGLE_APP_DESC_EMBEDDED`;