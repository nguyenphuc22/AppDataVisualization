import streamlit as st
from DataManager.ProductManager import ProductManager
from String import StringManager

def visualizationProductScreen(strings: StringManager):
    st.title(strings.get_string("data_visualization_title"))
    productManager = ProductManager.get_instance()
    data = productManager.get_data()

    # Check if DataFrame is empty and update the message accordingly
    if data.empty:
        message = strings.get_string("data_visualization_empty_message")
    else:
        message = strings.get_string("data_visualization_message")

    st.write(message)
    if not data.empty:
        st.dataframe(data)
