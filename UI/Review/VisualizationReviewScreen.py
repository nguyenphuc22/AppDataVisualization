import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import numpy as np

from DataManager.ReviewManager import ReviewManager
from String import StringManager
from AppContext import AppContext


def visualizationReviewScreen(strings: StringManager):
    print("visualization Review Screen Entry")
    st.title(strings.get_string("data_visualization_title"))
    st.write(strings.get_string("data_visualization_message"))

    # Update AppContext
    app_context = AppContext.get_instance()
    app_context.titlePage = "Trực quan hóa dữ liệu đánh giá"
    app_context.content = "Khám phá và phân tích dữ liệu đánh giá thông qua các biểu đồ trực quan."

    reviewManager = ReviewManager.get_instance()
    data = reviewManager.get_data()

    # Tạo data summary
    data_summary = data.describe()
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    categorical_columns = data.select_dtypes(include=['object']).columns

    summary_text = "Tóm tắt dữ liệu đánh giá:\n"
    summary_text += f"- Số lượng đánh giá: {len(data)}\n"
    summary_text += f"- Số cột số: {len(numeric_columns)}\n"
    summary_text += f"- Số cột phân loại: {len(categorical_columns)}\n"

    for col in numeric_columns:
        summary_text += f"- {col}: Trung bình = {data_summary[col]['mean']:.2f}, Min = {data_summary[col]['min']:.2f}, Max = {data_summary[col]['max']:.2f}\n"

    app_context.hyphothesisTitle = "Phân tích xu hướng đánh giá và tóm tắt dữ liệu"
    app_context.hyphothesisContent = summary_text

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

            # Phân tích
            rating_counts = data[x_column].value_counts().sort_index()
            most_common_rating = rating_counts.idxmax()
            chart_summary = f"\nPhân tích biểu đồ cột - Số lượng đánh giá:\n"
            chart_summary += f"- Rating phổ biến nhất: {most_common_rating} (số lượng: {rating_counts[most_common_rating]})\n"
            chart_summary += f"- Tỷ lệ đánh giá tích cực (4-5 sao): {(rating_counts[4] + rating_counts[5]) / len(data):.2%}\n"
        else:  # "Tần suất likeCount theo rating"
            sns.barplot(x=x_column, y=y_column, data=data, palette='Set2', ax=ax)
            ax.set_title('Tần suất likeCount theo rating')
            ax.set_xlabel('Rating')
            ax.set_ylabel('Số lượng like')

            # Phân tích
            avg_likes_by_rating = data.groupby('rating')['likeCount'].mean()
            max_likes_rating = avg_likes_by_rating.idxmax()
            chart_summary = f"\nPhân tích biểu đồ cột - Tần suất likeCount theo rating:\n"
            chart_summary += f"- Rating có trung bình số lượng like cao nhất: {max_likes_rating} (trung bình: {avg_likes_by_rating[max_likes_rating]:.2f})\n"
            chart_summary += f"- Có mối quan hệ tích cực giữa rating và số lượng like\n"
    elif chart_type == "Biểu đồ phân tán":
        sns.scatterplot(x=x_column, y=y_column, data=data, ax=ax)
        ax.set_title(f"Biểu đồ phân tán giữa {x_column} và {y_column}")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        # Phân tích
        correlation = data[[x_column, y_column]].corr().iloc[0, 1]
        chart_summary = f"\nPhân tích biểu đồ phân tán:\n"
        chart_summary += f"- Hệ số tương quan giữa {x_column} và {y_column}: {correlation:.2f}\n"
        if abs(correlation) > 0.5:
            chart_summary += f"- Có mối quan hệ {('tích cực' if correlation > 0 else 'tiêu cực')} mạnh giữa {x_column} và {y_column}\n"
        else:
            chart_summary += f"- Không có mối quan hệ mạnh giữa {x_column} và {y_column}\n"
    else:  # "Word Cloud"
        text = ' '.join(data[review_content_column].dropna())
        wordcloud = WordCloud(width=800, height=800, background_color='white').generate(text)

        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud của Review Content')
        st.pyplot(plt)

        # Phân tích
        word_freq = WordCloud().process_text(text)
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        chart_summary = f"\nPhân tích Word Cloud:\n"
        chart_summary += "- Top 5 từ xuất hiện nhiều nhất trong đánh giá:\n"
        for word, freq in top_words:
            chart_summary += f"  + {word}: {freq} lần\n"

    if chart_type != "Word Cloud":
        plt.tight_layout()
        st.pyplot(fig)

    plt.savefig('ChatBotUtils/image/data_visuallization.png')
    # Cập nhật AppContext với phân tích biểu đồ
    app_context.hyphothesisContent += chart_summary