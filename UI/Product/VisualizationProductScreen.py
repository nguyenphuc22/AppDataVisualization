import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from AppContext import AppContext
from DataManager.ProductManager import ProductManager
from String import StringManager


def visualizationProductScreen(strings: StringManager):
    print("visualization Product Screen Entry")
    st.title(strings.get_string("data_visualization_title"))
    st.write(strings.get_string("data_visualization_message"))

    # Update AppContext
    app_context = AppContext.get_instance()
    app_context.titlePage = "Trực quan hóa dữ liệu sản phẩm"
    app_context.content = "Khám phá và phân tích dữ liệu sản phẩm thông qua các biểu đồ trực quan."

    productManager = ProductManager.get_instance()
    data = productManager.get_data()

    # Tạo data summary
    data_summary = data.describe()
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    categorical_columns = data.select_dtypes(include=['object']).columns

    summary_text = "Tóm tắt dữ liệu:\n"
    summary_text += f"- Số lượng mẫu: {len(data)}\n"
    summary_text += f"- Số cột số: {len(numeric_columns)}\n"
    summary_text += f"- Số cột phân loại: {len(categorical_columns)}\n"

    for col in numeric_columns:
        summary_text += f"- {col}: Trung bình = {data_summary[col]['mean']:.2f}, Min = {data_summary[col]['min']:.2f}, Max = {data_summary[col]['max']:.2f}\n"

    app_context.hyphothesisTitle = "Phân tích xu hướng bán hàng và tóm tắt dữ liệu"
    app_context.hyphothesisContent = summary_text

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
    plt.savefig('ChatBotUtils/image/data_visuallization.png')

    # Update AppContext based on the selected chart
    chart_summary = f"\nPhân tích {chart_type.lower()}:\n"
    chart_summary += f"Biểu đồ này cho thấy mối quan hệ giữa {x_column} và {y_column}, "
    chart_summary += f"giúp chúng ta hiểu rõ hơn về xu hướng trong dữ liệu sản phẩm.\n"

    if chart_type == "Biểu đồ cột":
        top_category = data[x_column].value_counts().index[0]
        chart_summary += f"Danh mục '{top_category}' có số lượng cao nhất trong {x_column}.\n"
    elif chart_type == "Biểu đồ phân tán":
        correlation = data[[x_column, y_column]].corr().iloc[0, 1]
        chart_summary += f"Hệ số tương quan giữa {x_column} và {y_column} là {correlation:.2f}.\n"
    else:  # "Biểu đồ violin"
        median_value = data.groupby(x_column)[y_column].median().sort_values(ascending=False).index[0]
        chart_summary += f"Danh mục '{median_value}' có giá trị trung vị cao nhất cho {y_column}.\n"

    app_context.hyphothesisContent += chart_summary