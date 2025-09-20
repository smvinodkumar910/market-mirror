# Market Mirror

## Introduction

This Project builds an application which helps corporations to understand what customers feel about their products, engaging with customers by replying to their reviews / queries with the help of Generative AI. This app also facilitates the corporations to explore the competitive alternate products available in the market and compare them with their own products and to get comprehensive improvement plan from Gen AI to stand as a Market Leader.

## Objective

In this project we are using Mobile Apps as a product and analysing user reviews on Mobile apps from Google Playstore. Also, we will be using App details from other platforms like Apple and Windows and compare their features with the apps in Goole Playstore to get comprehensive improvement plan from Gemini.

## Data Collection

The project utilizes several publicly available datasets from Kaggle to source app information and user reviews across different platforms. The entire data collection and loading process is automated in the `01_load_data.ipynb` notebook.

**Data Sources:**

We use the following 5 Kaggle datasets:

**Reviews Datasets:**
*   Used to analyze user sentiment and feedback.
    1.  [google-play-store-apps](https://www.kaggle.com/datasets/lava18/google-play-store-apps)
    2.  [google-play-reviews](https://www.kaggle.com/datasets/marianna13/google-play-reviews)

**Product Details Datasets:**
*   Used for competitive analysis by comparing app features across platforms.
    1.  [google-play-store-apps](https://www.kaggle.com/datasets/maryamsayagh1/google-play-store-apps)
    2.  [app-store-apple-data-set-10k-apps](https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps)
    3.  [windows-store-top-apps-games](https://www.kaggle.com/datasets/quadeer15sh/windows-store-top-apps-games)

**Loading Process (BRONZE Layer):**

The data is loaded into a BigQuery dataset named `APP_MARKET_BRONZE`, which serves as our raw data layer, following a Medallion architecture. The process involves these steps:

1.  **Environment Setup:** A GCS bucket is created to stage the raw data files, and three BigQuery datasets (`APP_MARKET_BRONZE`, `APP_MARKET_SILVER`, `APP_MARKET_GOLD`) are prepared.
2.  **Download from Kaggle:** The datasets are downloaded from Kaggle using the `kagglehub` library.
3.  **Upload to GCS:** The downloaded CSV files are uploaded to the designated GCS bucket for staging.
4.  **Load into BigQuery:** The staged files in GCS are loaded into tables in the `APP_MARKET_BRONZE` dataset. This is done using `BigFrames` for the review datasets and a `Dataproc Spark` session for the product datasets to handle schema and column name adjustments.

The notebook detailing these steps can be found here:
[backend/01_load_data.ipynb](https://github.com/smvinodkumar910/market-mirror/blob/main/backend/01_load_data.ipynb)

## Data Processing

### Exploring data

The data exploration and preprocessing phase focuses on cleaning the raw data from the BRONZE layer, selecting relevant features, and structuring it into a more usable format in the SILVER layer. This process is detailed in the `02_explore_data.ipynb` notebook.

The key steps are:

*   **Combining and Cleaning Review Data:**
    *   Two separate Google Play Store review datasets (`google_play_reviews` and `googleplaystore_user_reviews`) are processed.
    *   Unnecessary columns are dropped, and column names are standardized for consistency (e.g., `App` to `app_name`, `Translated_Review` to `review_text`).
    *   The two cleaned datasets are then combined into a single, unified review table named `T_APP_REVIEWS` in the SILVER layer. This table consolidates all app reviews for easier analysis.

*   **Processing Product Information:**
    *   App information from three different platforms (Google, Apple, and Windows) is handled separately.
    *   **Google Play:** From the `cleanapp` table, essential details like `title`, `description`, `summary`, `ratings`, `reviews`, `price`, `free`, and `genre` are selected and saved into the `T_GOOGLE_APP_DETAILS` table in the SILVER layer.
    *   **Apple App Store:** Information is spread across two tables, `AppleStore` (metadata) and `appleStore_description` (text descriptions). These are joined on the app `id`. Key columns are selected, and the combined data is saved as `T_APPLE_APP_DETAILS` in the SILVER layer.
    *   **Windows Store:** The `windows_store` table is processed to keep relevant columns such as `Name`, `Price`, `Description`, `Category`, and `Size`, which are then saved to the `T_WINDOWS_APP_DETAILS` table in the SILVER layer.

*   **Setting up for AI Enrichment:**
    *   As part of the data processing workflow, BigQuery remote models are created to connect to Vertex AI's Generative AI capabilities.
    *   An embedding model (`text-embedding-005`) and a generative model (`gemini-2.0-flash`) are set up. These models are intended for later use in enriching the data, such as generating embeddings for app descriptions and analyzing review sentiments.

This structured approach ensures that the SILVER layer contains clean, well-organized data ready for the final processing and analysis steps in the GOLD layer.

Each step is explained in more detail in the notebook here:

The notebook detailing these steps can be found here:
[backend/02_explore_data.ipynb](https://github.com/smvinodkumar910/market-mirror/blob/main/backend/02_explore_data.ipynb)

### Data Processing 1: Enriching Review Data with Generative AI

This phase, detailed in the `03_processing_data_01.ipynb` notebook, focuses on cleaning and enriching the consolidated `T_APP_REVIEWS` table from the SILVER layer. The raw combined data suffered from many missing values, particularly in the `app_genre` and `sentiment` columns, which are critical for analysis.

To address this, we employed Generative AI through both BigFrames and BigQuery ML native functions.

**1. Predicting Missing App Genres with `bigframes.llm`:**

*   **Problem:** A significant number of reviews were missing an associated `app_genre`.
*   **Solution:** We used the `bigframes.ml.llm` module to predict the missing genres.
    *   A `GeminiTextGenerator` was initialized to connect to the `gemini-2.0-flash` model.
    *   For each app with a missing genre, a dynamic prompt was constructed asking the model to classify the app into one of the known genres.
    *   The `model.predict()` function was executed on a BigFrame containing these prompts. This function efficiently scales the inference process by translating the DataFrame operation into a BigQuery `ML.GENERATE_TEXT` SQL query, running the predictions in parallel directly within the data warehouse.
    *   The predicted genres were then used to fill the null values in the `app_genre` column.

**2. Generating Sentiments with BigQuery ML `AI.GENERATE`:**

*   **Problem:** While some reviews came with a pre-existing sentiment, many did not.
*   **Solution:** We leveraged the native `AI.GENERATE` SQL function in BigQuery to perform sentiment analysis at scale.
    *   A SQL query was run on all reviews where the `sentiment` was null.
    *   The `AI.GENERATE` function was called for each row, passing a prompt that instructed the Gemini model to classify the `review_text` as 'Positive', 'Negative', or 'Neutral'.
    *   This approach allows the database itself to orchestrate the calls to the LLM, enriching the data in place without needing to move it out of BigQuery.
    *   The results were used to update the `sentiment` column, ensuring every review has a corresponding sentiment value.

After these enrichment steps, the final, cleaned table is saved as `T_APP_REVIEWS_CLEANED` in the SILVER layer, ready for more advanced analysis and use in the application.

The notebook detailing these steps can be found here:
[backend/03_processing_data_01.ipynb](https://github.com/smvinodkumar910/market-mirror/blob/main/backend/03_processing_data_01.ipynb)

### Data Processing 2: Standardizing Product Data with Generative AI

This processing stage, covered in the `04_processing_data_02.ipynb` notebook, focuses on transforming the various product detail tables from the SILVER layer into a standardized format. The goal is to create a uniform schema across the Google, Windows, and Apple app datasets to enable direct comparisons.

The target schema includes the columns: `app_name`, `app_genre`, `app_description`, `app_price`, `free_flag`, and `app_rating`.

While the Google and Apple datasets required straightforward column renaming, the Windows dataset presented a unique challenge.

**Extracting Numeric Prices with BigQuery ML `AI.GENERATE_INT`:**

*   **Problem:** The `Price` column in the Windows app data was a free-form string containing text like "Free", "₹ 379.00", or even complex discount information. This made it impossible to use for numerical comparisons.
*   **Solution:** We leveraged the native BigQuery ML function `AI.GENERATE_INT` to intelligently parse these strings and extract a clean integer price.
    *   A SQL query was executed on the records that were not free.
    *   The `AI.GENERATE_INT` function was called for each row, passing a prompt that instructed the Gemini model to read the unstructured text and return only the numerical price of the app.
    *   This specialized function is optimized for extracting integer values from text, making it highly effective for this type of data cleaning and enrichment task. The entire operation runs within BigQuery, transforming the data at scale without external processing.
    *   The extracted integer price was then used to create a clean, numeric `app_price` column for the Windows dataset.

After this enrichment, all three platform-specific tables were saved with a uniform schema to both the SILVER layer (with a `_CLEANED` suffix) and the GOLD layer (with a `_FINAL` suffix), making them ready for the final analysis and application frontend.

The notebook detailing these steps can be found here:
[backend/04_processing_data_02.ipynb](https://github.com/smvinodkumar910/market-mirror/blob/main/backend/04_processing_data_02.ipynb)