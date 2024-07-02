import streamlit as st
from String import StringManager

def reviewScreen(strings: StringManager):
    st.title(strings.get_string(key="review_title"))
    st.write(strings.get_string(key="review_page_message"))
