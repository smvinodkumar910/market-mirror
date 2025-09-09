

CREATE OR REPLACE VECTOR INDEX APPLE_VECTOR_INDEX
ON `market-mirror-dev.APP_MARKET_GOLD.T_APPLE_APP_DESC_EMBEDDED`(ml_generate_embedding_result)
OPTIONS (distance_type = 'COSINE', index_type = 'IVF');

CREATE OR REPLACE VECTOR INDEX GOOGLE_VECTOR_INDEX
ON `market-mirror-dev.APP_MARKET_GOLD.T_GOOGLE_APP_DESC_EMBEDDED`(ml_generate_embedding_result)
OPTIONS (distance_type = 'COSINE', index_type = 'IVF');

---SELECT * FROM `market-mirror-dev.APP_MARKET_GOLD.INFORMATION_SCHEMA.VECTOR_INDEXES`

