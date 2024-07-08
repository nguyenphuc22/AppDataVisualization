import pandas as pd
import streamlit as st

from AppContext import AppContext
from DataManager.ProductManager import ProductManager
from DataManager.ReviewManager import ReviewManager
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

# Create an instance of StringManager
strings = StringManager.get_instance()
productManager = ProductManager.get_instance()
reviewManager = ReviewManager.get_instance()
appContext = AppContext.get_instance()

def main():
    uploadFilesView(strings)

    menu = st.sidebar.selectbox(
        strings.get_string("menu_title"),
        strings.get_string("menu_options"),
    )

    print(f"Selected menu: {menu}")

    if menu == strings.get_string("home_title"):
        set_title_and_screen(strings.get_string("home_title"), homeScreen)
        
    elif menu in [strings.get_string("product_title"), strings.get_string("review_title")]:
        handle_menu(menu)

    chatbotView()
    execute_screen()

def handle_menu(menu):
    menu_options = {
        strings.get_string("product_title"): {
            "options": strings.get_string("product_options"),
            "hypothesis_titles": strings.get_string("product_hypothesis_title"),
            "default_title": strings.get_string("product_title")
        },
        strings.get_string("review_title"): {
            "options": strings.get_string("review_options"),
            "hypothesis_titles": strings.get_string("review_hypothesis_title"),
            "default_title": strings.get_string("review_title")
        }
    }

    selected_option = st.sidebar.selectbox(
        menu,
        menu_options[menu]["options"]
    )
    print(f"Selected option menu: {selected_option}")

    if selected_option == strings.get_string("data_visualization_title"):
        appContext.titlePage = menu_options[menu]["default_title"]
        print(f"Set titlePage to: {appContext.titlePage}")
    elif selected_option == strings.get_string("hypothesis_title"):
        hypothesis_menu = st.sidebar.selectbox(
            strings.get_string("hypothesis_title"),
            menu_options[menu]["hypothesis_titles"]
        )
        print(f"Selected hypothesis_menu: {hypothesis_menu}")

        if hypothesis_menu in menu_options[menu]["hypothesis_titles"]:
            appContext.titlePage = hypothesis_menu
            print(f"Set titlePage to: {appContext.titlePage}")

def set_title_and_screen(title, screen_function):
    appContext.titlePage = title
    print(f"Set titlePage to: {appContext.titlePage}")
    screen_function(strings)

def execute_screen():
    print(f"Final titlePage: {appContext.titlePage}")

    screen_mapping = {
        strings.get_string("product_title"): visualizationProductScreen,
        strings.get_string("product_hypothesis_title")[0]: hypothesisProductScreenPhuc,
        strings.get_string("product_hypothesis_title")[1]: hypothesisProductScreenThanh,
        strings.get_string("product_hypothesis_title")[2]: hypothesisProductScreenBinh,
        strings.get_string("review_title"): visualizationReviewScreen,
        strings.get_string("review_hypothesis_title")[0]: hypothesisReviewScreenNhi,
        strings.get_string("review_hypothesis_title")[1]: hypothesisReviewScreenVien
    }

    screen_function = screen_mapping.get(appContext.titlePage)
    if screen_function:
        print(f"Executing {screen_function.__name__}")
        screen_function(strings)

if __name__ == "__main__":
    productManager.read_data("Data/filtered_data_product.xlsx")
    reviewManager.read_data("Data/filtered_data_review.xlsx")
    main()
    print("===========================================")
