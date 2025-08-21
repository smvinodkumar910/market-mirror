import streamlit as st
import pandas as pd


st.sidebar.header("App Reviews")
st.title("Review Engagement")



# review_to_show = st.selectbox("Select a review to respond to:", df['review'])

# st.subheader("Selected Review:")
# st.write(review_to_show)


# st.subheader("Your Response:")
# response = st.text_area("Write your reply here")

# if st.button("Submit Response"):
#     if response:
#         st.success("Response submitted successfully!")
#         # Here you would typically save the response to your database
#         st.write(f"Response to review: '{review_to_show}'")
#         st.write(f"Your response: '{response}'")
#     else:
#         st.warning("Please write a response before submitting.")
