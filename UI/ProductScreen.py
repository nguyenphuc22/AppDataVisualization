import streamlit as st
from DataManager.ProductManager import ProductManager
from String import StringManager


def productScreen():
    st.title(StringManager.get_string("product_title"))
    st.write(StringManager.get_string("product_page_message"))