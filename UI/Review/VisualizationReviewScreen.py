import streamlit as st
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
    st.subheader("Bảng dữ liệu đánh giá")
    st.dataframe(data)

    # Tạo sidebar cho người dùng chọn dạng biểu đồ và các trường dữ liệu
    st.sidebar.header("Tùy chọn trực quan hóa")
    chart_type = st.sidebar.radio("Chọn dạng biểu đồ",
                                  ("Biểu đồ cột", "Biểu đồ phân tán", "Word Cloud"))

    if chart_type == "Biểu đồ cột":
        bar_chart_option = st.sidebar.radio("Chọn loại biểu đồ cột",
                                            ("Số lượng đánh giá", "Tần suất likeCount theo rating"))
        if bar_chart_option == "Số lượng đánh giá":
            x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['rating'])
            y_column = 'rating'
        else:  # "Tần suất likeCount theo rating"
            x_column = 'rating'
            y_column = 'likeCount'
    elif chart_type == "Biểu đồ phân tán":
        x_column = st.sidebar.selectbox("Chọn trường dữ liệu cho trục x", ['likeCount', 'rating'])
        y_column = 'rating'
    else:  # "Word Cloud"
        review_content_column = st.sidebar.selectbox("Chọn trường dữ liệu cho Word Cloud", ['reviewContent'])

    # Tạo biểu đồ tương ứng dựa trên lựa chọn của người dùng
    st.subheader(f"{chart_type} cho dữ liệu đánh giá")
    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == "Biểu đồ cột":
        if bar_chart_option == "Số lượng đánh giá":
            sns.countplot(x=x_column, data=data, ax=ax)
            ax.set_title(f"Số lượng đánh giá theo {x_column}")
            ax.set_xlabel(x_column)
            ax.set_ylabel("Số lượng")
        else:  # "Tần suất likeCount theo rating"
            sns.barplot(x=x_column, y=y_column, data=data, palette='Set2', ax=ax)
            ax.set_title('Tần suất likeCount theo rating')
            ax.set_xlabel('Rating')
            ax.set_ylabel('Số lượng like')
    elif chart_type == "Biểu đồ phân tán":
        sns.scatterplot(x=x_column, y=y_column, data=data, ax=ax)
        ax.set_title(f"Biểu đồ phân tán giữa {x_column} và {y_column}")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
    else:  # "Word Cloud"
        text = ' '.join(data[review_content_column].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud của Review Content')
        st.pyplot(plt)

    if chart_type != "Word Cloud":
        plt.tight_layout()
        st.pyplot(fig)