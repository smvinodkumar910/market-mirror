
--create embedding models
CREATE OR REPLACE MODEL `{BQ_SILVER_DATASET}.embeddings`
REMOTE WITH CONNECTION `us.vertex-remote-models`
OPTIONS (ENDPOINT = 'text-embedding-005');


--create llm model for translation and summarization / text generation
CREATE OR REPLACE MODEL `{BQ_SILVER_DATASET}.gemini`
REMOTE WITH CONNECTION `us.vertex-remote-models`
OPTIONS (ENDPOINT = 'gemini-2.0-flash');

