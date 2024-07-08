import streamlit as st
from DataManager.ReviewManager import ReviewManager
from String import StringManager


def visualizationReviewScreen(strings: StringManager):
    st.title(strings.get_string("data_visualization_title"))
    st.write(strings.get_string("data_visualization_message"))
    reviewManager = ReviewManager.get_instance()
    data = reviewManager.get_data()
    st.write("DCM hien len chua:")
    st.dataframe(data)
