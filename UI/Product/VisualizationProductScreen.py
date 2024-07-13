import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from DataManager.ProductManager import ProductManager
from String import StringManager


def visualizationProductScreen(strings: StringManager):
    print("visualization Product Screen Entry")
    st.title(strings.get_string("data_visualization_title"))
    st.write(strings.get_string("data_visualization_message"))

    productManager = ProductManager.get_instance()
    data = productManager.get_data()

    # Hiển thị bảng dữ liệu
    st.subheader("Bảng dữ liệu sản phẩm")
    st.dataframe(data)

    # Tạo sidebar cho người dùng chọn dạng biểu đồ và các trường dữ liệu
    st.sidebar.header("Tùy chọn trực quan hóa")
    chart_type = st.sidebar.radio("Chọn dạng biểu đồ",
                                  ("Biểu đồ cột", "Biểu đồ phân tán", "Biểu đồ violin"))

    if chart_type == "Biểu đồ cột":
        x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['brandName', 'location'])
        y_column = 'itemSoldCntShow'
    elif chart_type == "Biểu đồ phân tán":
        x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['priceShow', 'ratingScore'])
        y_column = 'itemSoldCntShow'
    else:  # "Biểu đồ violin"
        x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['brandName', 'category'])
        y_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục y", ['priceShow', 'originalPrice'])

    # Tạo biểu đồ tương ứng dựa trên lựa chọn của người dùng
    st.subheader(f"{chart_type} cho dữ liệu sản phẩm")
    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == "Biểu đồ cột":
        sns.countplot(x=x_column, data=data, ax=ax)
        ax.set_title(f"Số lượng sản phẩm bán ra theo {x_column}")
        ax.set_xlabel(x_column)
        ax.set_ylabel("Số lượng")
    elif chart_type == "Biểu đồ phân tán":
        sns.scatterplot(x=x_column, y=y_column, data=data, ax=ax)
        ax.set_title(f"Biểu đồ phân tán giữa {x_column} và {y_column}")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
    else:  # "Biểu đồ violin"
        sns.violinplot(x=x_column, y=y_column, data=data, ax=ax)
        ax.set_title(f"Phân phối {y_column} theo {x_column}")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

    plt.tight_layout()
    st.pyplot(fig)