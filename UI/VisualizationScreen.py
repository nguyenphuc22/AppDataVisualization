import streamlit as st
from DataManager.ProductManager import ProductManager
from String import StringManager

def visualizationScreen(strings: StringManager):
    st.title(strings.get_string("data_visualization_title"))
    st.write(strings.get_string("data_visualization_message"))
    productManager = ProductManager.get_instance()
    data = productManager.get_data()
    st.dataframe(data)
