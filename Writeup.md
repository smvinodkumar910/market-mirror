# Market Mirror

## Introduction

This Project builds an application which helps corporations to understand what customers feel about their products, engaging with customers by replying to their reviews / queries with the help of Generative AI. This app also facilitates the corporations to explore the competitive alternate products available in the market and compare them with their own products and to get comprehensive improvement plan from Gen AI to stand as a Market Leader.

## Objective

In this project we are using Mobile Apps as a product and analysing user reviews on Mobile apps from Google Playstore. Also, we will be using App details from other platforms like Apple and Windows and compare their features with the apps in Goole Playstore to get comprehensive improvement plan from Gemini.

## Data Collection

We are going to use below 5 Kaggle Datasets for this project.

**Reviews Dataset :**
1. https://www.kaggle.com/datasets/lava18/google-play-store-apps
2. https://www.kaggle.com/datasets/marianna13/google-play-reviews

**Product Details Dataset:**
1. https://www.kaggle.com/datasets/maryamsayagh1/google-play-store-apps
2. https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps
3. https://www.kaggle.com/datasets/quadeer15sh/windows-store-top-apps-games

This Notebook explains the steps to load data into BQ as BRONZE LAYER:

https://github.com/smvinodkumar910/market-mirror/blob/main/backend/01_load_data.ipynb

## Data Processing

### Exploring data

We are exploring the data loaded into BRONZE Layer, clean it, removing unnecessary columns and then loading them into SILVER layer.
Each step explained in the notebook here:

https://github.com/smvinodkumar910/market-mirror/blob/main/backend/02_explore_data.ipynb

### Data Processing 1

