import streamlit as st

from DataManager.ProductManager import ProductManager
from DataManager.ReviewManager import ReviewManager
from String import StringManager
from UI.HomeScreen import homeScreen
from UI.HypothesisScreen import hypothesisScreen
from UI.ReviewScreen import reviewScreen
from UI.VisualizationScreen import visualizationScreen

# Create an instance of StringManager
strings = StringManager()
productManager = ProductManager.get_instance()
reviewManager = ReviewManager.get_instance()

def main():
    menu = st.sidebar.selectbox(
        strings.get_string("menu_title"),
        strings.get_string("menu_options")
    )

    if menu == strings.get_string("home_title"):
        homeScreen(strings)
    elif menu == strings.get_string("product_title"):
        product_menu = st.sidebar.selectbox(
            strings.get_string("product_title"),
            strings.get_string("product_options")
        )
        if product_menu == strings.get_string("data_visualization_title"):
            visualizationScreen(strings)
        elif product_menu == strings.get_string("hypothesis_title"):
            hypothesisScreen(strings)
    elif menu == strings.get_string("review_title"):
        reviewScreen()

if __name__ == "__main__":
    productManager.read_data("Data/filtered_data_product.xlsx")
    reviewManager.read_data("Data/filtered_data_review.xlsx")
    main()