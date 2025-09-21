
# Building Market Mirror: A Deep Dive into AI-Powered App Market Analysis

*A step-by-step guide to how we built an AI-powered application to understand customer sentiment, engage with users, and perform deep competitive analysis using Gemini, BigQuery, and LangGraph.*

---

In today's crowded digital marketplace, understanding what your customers think and what your competitors are doing is more critical than ever. For mobile app developers and product managers, this means sifting through thousands of reviews, trying to gauge sentiment, and manually scouting for competing apps. It's a daunting task.

What if you could automate this process? What if you could have an AI assistant that not only analyzes customer feedback but also provides a detailed competitive analysis and a strategic plan for improvement?

That's exactly what we set out to build with **Market Mirror**, an open-source application designed to do just that. In this post, we'll walk you through how we built it, from the ground up.

## The Blueprint: Our Data Foundation

Every great analytics application starts with a solid data foundation. For Market Mirror, we needed data on app details and user reviews from multiple platforms.

#### Sourcing the Data

We turned to Kaggle and sourced several publicly available datasets for the Google Play Store, Apple App Store, and Windows Store. This gave us a rich collection of app information and user reviews to work with.

#### The Medallion Architecture in BigQuery

Raw data is messy. To tame it, we adopted the **Medallion Architecture** in Google BigQuery, organizing our data into three layers:

*   **Bronze (Raw Data):** We started by loading the raw, untouched data from Kaggle into a BigQuery dataset named `APP_MARKET_BRONZE`. This layer serves as our single source of truth.
*   **Silver (Cleaned & Enriched):** This is where the magic begins. We cleaned the raw data, standardized column names, and combined datasets. For example, we merged two different Google Play review datasets into a single, unified table.
*   **Gold (Aggregated & Ready for Analysis):** In the final layer, we created aggregated tables optimized for our application. For instance, we created a table that summarizes review sentiments for each app, making it easy to quickly see which apps are most popular.

This structured approach ensures that our data is clean, reliable, and ready for the complex analysis to come.

## The Magic Wand: Enriching Data with Generative AI

Our raw data had a lot of missing pieces. Many reviews were missing an `app_genre` or a `sentiment` score. The `Price` column in the Windows dataset was a mess of free-form text like "Free" or "₹ 379.00".

This is where **Gemini**, Google's powerful generative AI model, came to the rescue, right within BigQuery.

#### Predicting Missing App Genres and Sentiments

Using `bigframes.llm` and BigQuery ML's native `ML.GENERATE_TEXT` function, we put Gemini to work. We created prompts that asked the model to classify apps into genres or to determine the sentiment of a review. The model then filled in the missing values with remarkable accuracy, running the predictions in parallel directly within our data warehouse.

#### Extracting Structured Data from Unstructured Text

For the messy `Price` column, we used a specialized function, `ML.GENERATE_INT`. We simply asked Gemini to read the unstructured text and return only the numerical price. This allowed us to create a clean, numeric `app_price` column, ready for numerical comparisons.

## The Brains of the Operation: Vector Search and LangGraph

The crown jewel of Market Mirror is its ability to perform deep competitive analysis. How do you find "similar" apps when "similar" can mean so many different things? The answer is **vector search**.

#### Creating and Indexing Embeddings

We used the `ML.GENERATE_EMBEDDING` function in BigQuery to create vector embeddings of each app's description. These embeddings are numerical representations of the text's meaning. We then created a **vector index** on these embeddings, allowing for lightning-fast similarity searches.

#### Orchestrating the Analysis with LangGraph

When a user wants to analyze an app, a sophisticated workflow built with **LangGraph** kicks into gear. LangGraph is a library that allows you to build complex, stateful applications with LLMs.

Here’s how our competitor analysis workflow runs:

1.  **Embedding Generation:** The description of the selected Google app is retrieved, and its vector embedding is generated.
2.  **Vector Similarity Search:** This embedding is used to perform a similarity search against our vector indexes for the Apple and Windows app stores. This is powered by **BigQuery Vector Search** and seamlessly integrated using the `BigQueryVectorStore` component from **LangChain**.
3.  **Information Retrieval:** The top similar apps from the other platforms are identified, and their details are retrieved from BigQuery.
4.  **Comprehensive Analysis with Gemini:** All this information—the original app and its competitors—is passed to a Gemini model. The model then generates a comprehensive report that includes:
    *   A feature-by-feature comparison.
    *   A summary of advantages and disadvantages.
    *   A strategic improvement plan for the selected app.

## The Face of the App: Our Streamlit Frontend

All this powerful backend processing is made accessible through a simple and intuitive multi-page Streamlit application.

*   **App Rankings:** A dashboard for visualizing app performance and sentiment.
*   **Review Engagement:** A tool for filtering reviews and generating AI-powered responses to customers.
*   **Competitor Analysis:** The heart of the app, where users can trigger the LangGraph workflow and get deep competitive insights.

To ensure a smooth user experience, the entire LangGraph workflow is cached using Streamlit's `@st.cache_resource`, which prevents the application from being re-initialized on every interaction, making the analysis fast and efficient.

## Conclusion

Market Mirror is a testament to the power of combining modern data architecture, generative AI, and open-source tools. By leveraging BigQuery's powerful features, the intelligence of Gemini, and the flexibility of LangGraph and Streamlit, we were able to build a powerful tool for app market analysis.

We believe this is just the beginning. The same principles and architecture could be applied to analyze any product with customer reviews, opening up a world of possibilities for data-driven decision-making.

---

**Interested in diving deeper?** Check out the complete project on our [GitHub repository](https://github.com/smvinodkumar910/market-mirror)!
