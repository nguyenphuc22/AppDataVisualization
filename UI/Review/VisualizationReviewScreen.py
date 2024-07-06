import streamlit as st
from String import StringManager


def visualizationReviewScreen(strings: StringManager):
    st.title(strings.get_string("data_visualization_title"))
    st.write(strings.get_string("data_visualization_message"))
