import streamlit as st
from DataManager.ReviewManager import ReviewManager
from String import StringManager

def visualizationReviewScreen(strings: StringManager):
    st.title(strings.get_string("data_visualization_title"))
    reviewManager = ReviewManager.get_instance()
    data = reviewManager.get_data()

    # Check if DataFrame is empty and update the message accordingly
    if data.empty:
        message = strings.get_string("data_visualization_empty_message")
    else:
        message = strings.get_string("data_visualization_message")

    st.write(message)
    if not data.empty:
        st.dataframe(data)
