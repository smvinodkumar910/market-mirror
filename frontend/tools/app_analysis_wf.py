from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore
from google.cloud import bigquery
from langchain_google_vertexai import ChatVertexAI
import os

import streamlit as st

from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages

from pydantic import BaseModel


# Get environment variables
PROJECT_ID = 'market-mirror-dev' #os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_REGION = 'US' #os.getenv("GOOGLE_CLOUD_REGION")
GOOGLE_GENAI_LOCATION = 'us-central1' # os.getenv("GOOGLE_GENAI_LOCATION")



BQ_BRONZE_DATASET = "APP_MARKET_BRONZE" 
BQ_SILVER_DATASET = "APP_MARKET_SILVER" 
BQ_GOLD_DATASET = "APP_MARKET_GOLD" 

google_apps_embed_tb = 'T_GOOGLE_APP_DESC_EMBEDDED'
apple_apps_embed_tb = 'T_APPLE_APP_DESC_EMBEDDED'
windows_apps_embed_tb = 'T_WINDOWS_APP_DESC_EMBEDDED'

@st.cache_resource
def get_workflow_app():
    #Creating llm object
    llm = ChatVertexAI(model='gemini-2.0-flash-001',location=GOOGLE_GENAI_LOCATION)

    # Defining a custom state object to hold
    class CustomState(BaseModel):
        messages: str = ''
        google_app_name: str = ''
        google_app_desc: str = ''
        query_vector: list | None = []
        top_k: int | None = 3
        windows_apps_list: str | None = ''
        apple_apps_list: str | None = ''
        windows_app_desc: list[dict] | None = []
        apple_app_desc: list[dict] | None = []
        summary: str | None = ''


    #creating embedding object
    embedding = VertexAIEmbeddings(
        model_name="text-embedding-005", project=PROJECT_ID
    )

    #Createing BigQueryVectorStore for each table separately
    #Apple vector store
    apple_apps_vector_store = BigQueryVectorStore(
        project_id=PROJECT_ID,
        dataset_name=BQ_GOLD_DATASET,
        table_name=apple_apps_embed_tb,
        location=GOOGLE_CLOUD_REGION,
        embedding=embedding,
    )

    #Windows vector store
    windows_apps_vector_store = BigQueryVectorStore(
        project_id=PROJECT_ID,
        dataset_name=BQ_GOLD_DATASET,
        table_name=windows_apps_embed_tb,
        location=GOOGLE_CLOUD_REGION,
        embedding=embedding,
    )

    def get_google_app_desc(state: CustomState):
        client = bigquery.Client(project=PROJECT_ID,location=GOOGLE_CLOUD_REGION)
        google_app=state.google_app_name

        sql_query = f"""select app_description from `market-mirror-dev.APP_MARKET_GOLD.T_GOOGLE_APP_DETAIL_FINAL` where app_name='{google_app}'"""

        app_desc = client.query(sql_query).to_dataframe()['app_description'][0]
        output = {f'google_app_desc' : app_desc}
        return output


    def generate_embeddings(state: CustomState):
      embeddings_list = embedding.embed_query(state.google_app_desc)
      return {'query_vector': embeddings_list}


    def make_vector_search(store,platform):
      def get_similar_apps(state: CustomState):
        top_k = state.top_k
        query_vector = state.query_vector
        docs = store.similarity_search_by_vector(embedding=query_vector, k=top_k)
        similar_apps = []
        for doc in docs:
          similar_apps.append(doc.page_content)
        apps_list_str = ",".join([f"'{app}'" for app in similar_apps])
        return {f'{platform}_apps_list':apps_list_str}
      return get_similar_apps


    apple_apps_search = make_vector_search(apple_apps_vector_store,'apple')
    windows_apps_search = make_vector_search(windows_apps_vector_store,'windows')


    def make_app_desc_function(table_id,platform):
      client = bigquery.Client(project=PROJECT_ID, location=GOOGLE_CLOUD_REGION)
      def get_app_desc(state: CustomState):
        list_of_apps=''
        if platform == 'windows':
          list_of_apps = state.windows_apps_list
        elif platform == 'apple':
          list_of_apps = state.apple_apps_list
        else:
          raise ValueError('Invalid platform')

        sql_query = f"""select * from {table_id} where app_name in ({list_of_apps})"""

        df = client.query(sql_query).to_dataframe()
        output = {f'{platform}_app_desc' : df.to_dict('records')}
        return output
      return get_app_desc

    get_apple_app_desc = make_app_desc_function('market-mirror-dev.APP_MARKET_GOLD.T_APPLE_APP_DETAIL_FINAL','apple')
    get_windows_app_desc = make_app_desc_function('market-mirror-dev.APP_MARKET_GOLD.T_WINDOWS_APP_DETAIL_FINAL','windows')


    def get_comparison_summary(state: CustomState):

      template = f"""
        You are a market research analyst.
        You will be provided with an app name and and its feature details from Goole Play Store.
        And similar {state.top_k} competitive apps providing same kind of functionalities will be provided from other platforms like Apple and Windows.
        You need to do the following:

        1. You need to analyse and compare the features of Google app vs Other competitive apps from apple/windows platform and a brief summary.
        2. Summarize the advantages of Google app vs Other competitive apps from apple/windows platform.
        3. Summarize the disadvantages/drawbacks of Google app vs Other competitive apps from apple/windows platform.
        4. Provie a comprehensive improvement plan for the Goole app to stand as a market leader.

        You have to evaluate the features of the apps, summarize them in bullet points for each app in each platform.

        Google App Details : app_name:{state.google_app_name}, app_description: {state.google_app_desc}
        Windows App Details : {state.windows_app_desc}
        Apple App Details : {state.apple_app_desc}
        """


      output = llm.invoke(template)

      
      return {"summary":output}



    # Define a new graph
    workflow = StateGraph(state_schema=CustomState)

    #Create nodes
    workflow.add_node("get_google_app_desc", get_google_app_desc)

    workflow.add_node("generate_query_embedding", generate_embeddings)

    workflow.add_node("windows_apps_search", windows_apps_search)
    workflow.add_node("apple_apps_search", apple_apps_search)

    workflow.add_node("get_windows_app_desc", get_windows_app_desc)
    workflow.add_node("get_apple_app_desc", get_apple_app_desc)

    workflow.add_node("get_comparison_summary", get_comparison_summary)

    #Create Edges
    workflow.add_edge(START, "get_google_app_desc")
    workflow.add_edge("get_google_app_desc", "generate_query_embedding")

    workflow.add_edge("generate_query_embedding", "windows_apps_search")
    workflow.add_edge("generate_query_embedding", "apple_apps_search")

    workflow.add_edge("windows_apps_search", "get_windows_app_desc")
    workflow.add_edge("apple_apps_search", "get_apple_app_desc")

    workflow.add_edge("get_windows_app_desc","get_comparison_summary")
    workflow.add_edge("get_apple_app_desc","get_comparison_summary")

    workflow.add_edge("get_comparison_summary", END)

    app = workflow.compile()
    return app

def get_competitor_summary(google_app_name:str):
    app = get_workflow_app()
    output = app.invoke(input={"google_app_name": google_app_name})
    return output['summary'].content