import os

def initialize_folder_api():
    directory = 'ChatBotUtils/image/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = "ChatBotUtils/privateInfo.py"
    if not os.path.exists(filename):
        api_key = input("Please enter your OpenAI API key: ").strip()
        with open(filename, "w") as file:
            file.write(f"OPENAI_API_KEY = \"{api_key}\"\n")
    else:
        from ChatBotUtils.privateInfo import OPENAI_API_KEY
        if OPENAI_API_KEY == "":
            api_key = input("Please enter your OpenAI API key: ").strip()
            with open(filename, "w") as file:
                file.write(f"OPENAI_API_KEY = \"{api_key}\"\n")
        else:
            print("OpenAI API key is already set in privateInfo.py.")

initialize_folder_api()

import streamlit as st

from AppContext import AppContext
from DataManager.ProductManager import ProductManager
from DataManager.ReviewManager import ReviewManager
from FixedContent import FixedContent
from String import StringManager
from UI.Component.ChatBotView import chatbotView
from UI.Component.UploadFilesView import uploadFilesView
from UI.HomeScreen import homeScreen
from UI.Product.Hypothesis.HypothesisProductScreenBinh import hypothesisProductScreenBinh
from UI.Product.Hypothesis.HypothesisProductScreenPhuc import hypothesisProductScreenPhuc
from UI.Product.Hypothesis.HypothesisProductScreenThanh import hypothesisProductScreenThanh
from UI.Product.VisualizationProductScreen import visualizationProductScreen
from UI.Review.Hypothesis.HypothesisReviewScreenNhi import hypothesisReviewScreenNhi
from UI.Review.Hypothesis.HypothesisReviewScreenVien import hypothesisReviewScreenVien
from UI.Review.VisualizationReviewScreen import visualizationReviewScreen
from ChatBot import build_database

# Create an instance of StringManager
strings = StringManager.get_instance()
productManager = ProductManager.get_instance()
reviewManager = ReviewManager.get_instance()
appContext = AppContext.get_instance()
fixedContent = FixedContent.get_instance()

def main():
    uploadFilesView(strings)
    build_database()

    menu = st.sidebar.selectbox(
        strings.get_string("menu_title"),
        strings.get_string("menu_options"),
    )

    print(f"Selected menu: {menu}")

    if menu == strings.get_string("home_title"):
        appContext.titlePage = strings.get_string("home_title")
        print(f"Set titlePage to: {appContext.titlePage}")
        homeScreen(strings)
        
    elif menu == strings.get_string("product_title"):
        product_menu = st.sidebar.selectbox(
            strings.get_string("product_title"),
            strings.get_string("product_options")
        )
        print(f"Selected product_menu: {product_menu}")

        if product_menu == strings.get_string("data_visualization_title"):
            appContext.titlePage = strings.get_string("product_title")
            print(f"Set titlePage to: {appContext.titlePage}")
        elif product_menu == strings.get_string("hypothesis_title"):
            product_hypothesis_menu = st.sidebar.selectbox(
                strings.get_string("hypothesis_title"),
                strings.get_string("product_hypothesis_title")
            )
            print(f"Selected product_hypothesis_menu: {product_hypothesis_menu}")

            if product_hypothesis_menu == strings.get_string("product_hypothesis_title")[0]:
                appContext.titlePage = strings.get_string("product_hypothesis_title")[0]
            elif product_hypothesis_menu == strings.get_string("product_hypothesis_title")[1]:
                appContext.titlePage = strings.get_string("product_hypothesis_title")[1]
            elif product_hypothesis_menu == strings.get_string("product_hypothesis_title")[2]:
                appContext.titlePage = strings.get_string("product_hypothesis_title")[2]
            print(f"Set titlePage to: {appContext.titlePage}")

    elif menu == strings.get_string("review_title"):
        review_menu = st.sidebar.selectbox(
            strings.get_string("review_title"),
            strings.get_string("review_options")
        )
        print(f"Selected review_menu: {review_menu}")

        if review_menu == strings.get_string("data_visualization_title"):
            appContext.titlePage = strings.get_string("review_title")
            print(f"Set titlePage to: {appContext.titlePage}")
        elif review_menu == strings.get_string("hypothesis_title"):
            review_hypothesis_menu = st.sidebar.selectbox(
                strings.get_string("hypothesis_title"),
                strings.get_string("review_hypothesis_title")
            )
            print(f"Selected review_hypothesis_menu: {review_hypothesis_menu}")

            if review_hypothesis_menu == strings.get_string("review_hypothesis_title")[0]:
                appContext.titlePage = strings.get_string("review_hypothesis_title")[0]
            elif review_hypothesis_menu == strings.get_string("review_hypothesis_title")[1]:
                appContext.titlePage = strings.get_string("review_hypothesis_title")[1]
            print(f"Set titlePage to: {appContext.titlePage}")


    print(f"Final titlePage: {appContext.titlePage}")

    if appContext.titlePage == strings.get_string("product_title"):
        print("Executing visualizationProductScreen")
        visualizationProductScreen(strings)
    elif appContext.titlePage == strings.get_string("product_hypothesis_title")[0]:
        hypothesisProductScreenPhuc(strings)
    elif appContext.titlePage == strings.get_string("product_hypothesis_title")[1]:
        hypothesisProductScreenThanh(strings)
    # elif appContext.titlePage == strings.get_string("product_hypothesis_title")[2]:
    #     hypothesisProductScreenBinh(strings)
    elif appContext.titlePage == strings.get_string("review_title"):
        print("Executing visualizationReviewScreen")
        visualizationReviewScreen(strings)
    elif appContext.titlePage == strings.get_string("review_hypothesis_title")[1]:
        hypothesisReviewScreenVien(strings)
    elif appContext.titlePage == strings.get_string("review_hypothesis_title")[0]:
        hypothesisReviewScreenNhi(strings)
    print("===========================================")

    chatbotView()

if __name__ == "__main__":
    print("Main Entry...")
    productManager.read_data("Data/filtered_data_product.xlsx")
    reviewManager.read_data("Data/filtered_data_review.xlsx")
    main()
