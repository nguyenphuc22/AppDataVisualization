import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from DataManager.ReviewManager import ReviewManager
from String import StringManager


def visualizationReviewScreen(strings: StringManager):
    print("visualization Review Screen Entry")
    st.title(strings.get_string("data_visualization_title"))
    st.write(strings.get_string("data_visualization_message"))

    reviewManager = ReviewManager.get_instance()
    data = reviewManager.get_data()

    # Hiển thị bảng dữ liệu
    st.subheader("Bảng dữ liệu đánh giá sản phẩm")
    st.dataframe(data)

    # Tạo sidebar cho người dùng chọn dạng biểu đồ và các trường dữ liệu
    st.sidebar.header("Tùy chọn trực quan hóa")
    chart_type = st.sidebar.radio("Chọn dạng biểu đồ",
                                  ("Biểu đồ cột", "Biểu đồ phân tán", "Biểu đồ violin", "Wordcloud"))

    if chart_type == "Biểu đồ cột":
        x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['rating', 'isPurchased'])
        y_column = 'likeCount'
    elif chart_type == "Biểu đồ phân tán":
        x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['rating', 'likeCount'])
        y_column = 'helpful'
    elif chart_type == "Biểu đồ violin":
        x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['rating', 'isGoodReview'])
        y_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục y", ['likeCount', 'helpful'])

    # Tạo biểu đồ tương ứng dựa trên lựa chọn của người dùng
    if chart_type in ["Biểu đồ cột", "Biểu đồ phân tán", "Biểu đồ violin"]:
        st.subheader(f"{chart_type} cho dữ liệu đánh giá sản phẩm")
        fig, ax = plt.subplots(figsize=(10, 6))

        if chart_type == "Biểu đồ cột":
            sns.countplot(x=x_column, data=data, ax=ax)
            ax.set_title(f"Số lượng đánh giá theo {x_column}")
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

    elif chart_type == "Wordcloud":
        st.subheader("Wordcloud cho nội dung đánh giá")
        # Tạo một chuỗi văn bản từ tất cả các đánh giá
        text = " ".join(data['reviewContent'].astype(str))

        # Tạo wordcloud
        wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(text)

        # Hiển thị wordcloud
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)

        st.pyplot(plt)