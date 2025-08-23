

SELECT
query.query,
base.app_name
FROM
    VECTOR_SEARCH(
        TABLE `market-mirror-dev.APP_MARKET_GOLD.T_WINDOWS_APP_DESC_EMBEDDED`,
        'ml_generate_embedding_result',
        (
            SELECT
                ml_generate_embedding_result,
                content AS query
            FROM
                ML.GENERATE_EMBEDDING(
                    MODEL `market-mirror-dev.APP_MARKET_SILVER.embeddings`,
                    (SELECT 'GenAI tool helps to create images for artists and media persons' AS content)
                )
        ),
        top_k => 5,
        options => '{"use_brute_force":true}'
    );


    --options => '{"fraction_lists_to_search": 0.01}'