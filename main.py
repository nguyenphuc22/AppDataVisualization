import streamlit as st
from streamlit_option_menu import option_menu


def home():
    st.title("Trang chủ")
    st.write("Chào mừng đến với ứng dụng của chúng tôi!")


def product():
    st.title("Sản phẩm")
    st.write("Đây là trang sản phẩm của chúng tôi.")
    # Thêm nội dung về sản phẩm ở đây


def review():
    st.title("Đánh giá")
    st.write("Đây là trang đánh giá của chúng tôi.")
    # Thêm form đánh giá hoặc hiển thị đánh giá ở đây


def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Danh Mục",
            options=["Trang chủ", "Sản phẩm", "Đánh giá"],
            icons=["house", "box", "star"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Trang chủ":
        home()
    elif selected == "Sản phẩm":
        product()
    elif selected == "Đánh giá":
        review()


if __name__ == "__main__":
    main()