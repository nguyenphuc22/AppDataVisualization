import streamlit as st
from String import StringManager


def reviewScreen():
    st.title(StringManager.get_string("review_title"))
    st.write(StringManager.get_string("review_page_message"))