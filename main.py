import pandas as pd
import streamlit as st

from DataManager.ProductManager import ProductManager
from DataManager.ReviewManager import ReviewManager
from String import StringManager
from UI.Component.UploadFilesView import uploadFilesView
from UI.HomeScreen import homeScreen
from UI.Product.Hypothesis.HypothesisProductScreenBinh import hypothesisProductScreenBinh
from UI.Product.Hypothesis.HypothesisProductScreenPhuc import hypothesisProductScreenPhuc
from UI.Product.Hypothesis.HypothesisProductScreenThanh import hypothesisProductScreenThanh
from UI.Product.VisualizationProductScreen import visualizationProductScreen
from UI.Review.Hypothesis.HypothesisReviewScreenNhi import hypothesisReviewScreenNhi
from UI.Review.Hypothesis.HypothesisReviewScreenVien import hypothesisReviewScreenVien
from UI.Review.VisualizationReviewScreen import visualizationReviewScreen

# Create an instance of StringManager
strings = StringManager.get_instance()
productManager = ProductManager.get_instance()
reviewManager = ReviewManager.get_instance()

def main():
    uploadFilesView(strings)

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
            visualizationProductScreen(strings)
        elif product_menu == strings.get_string("hypothesis_title"):
            product_hypothesis_menu = st.sidebar.selectbox(
                strings.get_string("hypothesis_title"),
                strings.get_string("product_hypothesis_title")
            )
            if product_hypothesis_menu == strings.get_string("product_hypothesis_title")[0]:
                hypothesisProductScreenPhuc(strings)
            elif product_hypothesis_menu == strings.get_string("product_hypothesis_title")[1]:
                hypothesisProductScreenThanh(strings)
            elif product_hypothesis_menu == strings.get_string("product_hypothesis_title")[2]:
                hypothesisProductScreenBinh(strings)

    elif menu == strings.get_string("review_title"):
        review_menu = st.sidebar.selectbox(
            strings.get_string("review_title"),
            strings.get_string("review_options")
        )
        if review_menu == strings.get_string("review_title"):
            visualizationReviewScreen(strings)
        elif review_menu == strings.get_string("hypothesis_title"):
            review_hypothesis_menu = st.sidebar.selectbox(
                strings.get_string("hypothesis_title"),
                strings.get_string("review_hypothesis_title")
            )
            if review_hypothesis_menu == strings.get_string("review_hypothesis_title")[1]:
                hypothesisReviewScreenVien(strings)
            elif review_hypothesis_menu == strings.get_string("review_hypothesis_title")[0]:
                hypothesisReviewScreenNhi(strings)


if __name__ == "__main__":
    productManager.read_data("Data/filtered_data_product.xlsx")
    reviewManager.read_data("Data/filtered_data_review.xlsx")
    main()