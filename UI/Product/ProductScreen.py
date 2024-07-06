import streamlit as st
from String import StringManager


def productScreen(strings: StringManager):
    st.title(strings.get_string("product_title"))
    st.write(strings.get_string("product_page_message"))