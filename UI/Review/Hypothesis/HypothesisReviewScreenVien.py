import streamlit as st
from String import StringManager
from DataManager.ReviewManager import ReviewManager
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from collections import Counter

def hypothesisReviewScreenVien(strings: StringManager):
    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("review_hypothesis_title")[1])

    # Lấy instance của ReviewManager
    review_manager = ReviewManager.get_instance()

    # Load dữ liệu (có thể đặt trong một hàm initialization riêng)
    if not hasattr(st.session_state, 'data_loaded'):
        try:
            review_manager.load_data("Data/filtered_data_review.xlsx")
            st.session_state.data_loaded = True
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return

    # Lấy dữ liệu
    df_new = review_manager.get_data()

    if df_new is None or df_new.empty:
        st.warning("No data available. Please check if data was loaded correctly.")
        return
    # Ghi tiêu đề
    st.markdown("## Phân tích dữ liệu dựa trên cảm xúc của người dùng tác động như thế nào đánh chỉ số đánh giá và các nhãn hàng lớn trên thế giới") 
    # Hiển thị tóm tắt dữ liệu
    st.write(review_manager.get_data_summary())

    # Visualization 1: Overall Sentiments
    st.subheader("Các cảm xúc tổng thể")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x="Sentiment", data=df_new, ax=ax, order=["Negative", "Neutral", "Positive"], palette="viridis")
    ax.set_xlabel("Cảm xúc", fontsize=12)
    ax.set_ylabel("Số lượng", fontsize=12)
    st.pyplot(fig)
    st.markdown("""
    **Nhận xét:** Cảm xúc tiêu cực chiếm khoảng 500 lượt trong dữ liệu, tương ứng với các cảm xúc trung lập và tiêu cực 
                lần lượt là vào khoảng 1500 lượt và 3000 lượt. Điều này cho ta thấy rằng các đánh giá tiêu cực chủ yếu đi 
                kèm với cảm xúc tiêu cực, trong khi đánh giá cao (4-5 sao) chủ yếu đi kèm với cảm xúc tích cực. Điều này 
                xác nhận rằng cảm xúc tích cực thường dẫn đến đánh giá cao và ngược lại.
    """)

    # Visualization 2: Overall Ratings
    st.subheader("Các đánh giá tổng thể")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x="rating", data=df_new, ax=ax, palette="viridis")
    ax.set_xlabel("Đánh giá", fontsize=12)
    ax.set_ylabel("Số lượng", fontsize=12)
    st.pyplot(fig)
    st.markdown("""
    **Nhận xét:** Đa số khách hàng đánh giá rất cao sản phẩm và dịch vụ, cho thấy được sự hài lòng cao. 
                Tuy nhiên ta cần tìm hiểu thêm các lý do tại sao vẫn có 1 số ít đánh giá thấp.
    """)

    # Visualization 3: Rating Frequency by Sentiment
    st.subheader("Tần suất đánh giá (%) theo cảm xúc")
    fig, ax = plt.subplots(figsize=(12, 8))
    percentstandardize_barplot(x="rating", y="Percentage", hue="Sentiment", data=df_new, ax=ax)
    ax.set_xlabel("Đánh giá")
    ax.set_ylabel("Phần trăm %")
    st.pyplot(fig)
    st.markdown("""
    **Nhận xét:** Biểu đồ tần suất đánh giá % theo cảm xúc cho thấy rằng đánh giá 1-2 sao chủ yếu là tiêu cực, 
                3-4 sao là trung lập và 5 sao có cả tiêu cực lẫn tích cực. Một số lý do có thể giải thích cảm xúc tích cực 
                trong đánh giá 1 sao bao gồm đánh giá dựa trên một khía cạnh cụ thể, sự thất vọng và việc gửi thông điệp 
                mạnh mẽ. Ngược lại, phản hồi tiêu cực trong đánh giá 5 sao có thể do tiêu chuẩn đánh giá khác nhau, cân 
                nhắc tổng thể, tâm lý “mềm lòng,” sự trung thành với thương hiệu và mong muốn khuyến khích cải thiện.
    """)

    # Word Clouds and Top Words
    st.subheader("Phân tích từ ngữ")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Các từ xuất hiện nhiều với cảm xúc tích cực")
        positive_wordcloud = create_wordcloud(df_new, review_manager.positive_words)
        st.image(positive_wordcloud.to_array())

        st.write("Top 20 từ tích cực")
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_top_words(df_new, review_manager.positive_words, ax, color='green')
        st.pyplot(fig)

    with col2:
        st.write("Các từ xuất hiện nhiều với cảm xúc tiêu cực")
        negative_wordcloud = create_wordcloud(df_new, review_manager.negative_words)
        st.image(negative_wordcloud.to_array())

        st.write("Top 20 từ tiêu cực")
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_top_words(df_new, review_manager.negative_words, ax, color='red')
        st.pyplot(fig)

    st.markdown("""
    **Nhận xét**: 
    - Các từ "Chất lượng" và "Uy tín" trong cảm xúc tích cực cho thấy sản phẩm/dịch vụ đáp ứng tốt tiêu chuẩn 
               và xây dựng niềm tin với khách hàng. "Nhanh", "nhanh chóng", "mới" nhấn mạnh sự nhanh nhẹn và mới mẻ, 
               trong khi "Hài lòng", "Tuyệt vời", "Cảm ơn", "Nhiệt tình" thể hiện sự hài lòng cao của khách hàng. 
               Các từ như "Rẻ" và "Hợp lý" cho thấy khách hàng quan tâm đến giá trị kinh tế. 
    - Ngược lại, các từ tiêu cực như "kém", "cũ", "hư", "không tốt", "lỗi", "hỏng" phản ánh chất lượng sản phẩm kém, 
               và "lừa đảo", "thất vọng", "ko đúng", "giao sai" thể hiện sự thất vọng về độ tin cậy và trung thực. 
               """)
    
    # Sentiment Analysis by Brand
    st.subheader("Tỷ lệ phần trăm theo cảm xúc cho từng thương hiệu")
    sentiment_percent = calculate_sentiment_percentage(df_new)
    fig, ax = plt.subplots(figsize=(14, 10))
    sentiment_percent.plot(kind='bar', stacked=True, colormap='plasma', ax=ax, edgecolor='black')
    ax.set_xlabel('Thương hiệu')
    ax.set_ylabel('Tỷ lệ phần trăm (%)')
    plt.xticks(rotation=45)
    ax.legend(title='Sentiment', labels=['Negative', 'Positive'])
    st.pyplot(fig)
    st.markdown("""
    **Nhận xét:** 
    - Tỷ lệ đánh giá tích cực vượt trội hoàn toàn so với tiêu cực.
    - Realme dẫn đầu ở mức tầm 95'%' cảm xúc tích cực. Theo sau là các hãng LG, Sony, Vsmart là trên 90'%'. 
                Tiếp theo là Apple, Samsung và các hãng khác nằm trong khoảng 80-90'%' .
    - Huawei và Xiaomi có điểm đánh giá tiêu cực cao nhất. Hãng đang đối với mặt với một vài thách thức về 
                hình ảnh và sự hài lòng của khách hàng
    - Các hãng của Trung Quốc như Realme, Oppo, Vivo đang tạo ấn tượng tốt với khách hàng.
    - 2 thương hiệu lớn Apple và Samsung vẫn đang giữ vị thế vững chắc nhưng đang phải đối mặt cao sự kỳ vọng của người dùng.
    """)

# Các hàm hỗ trợ (giữ nguyên như cũ)
def percentstandardize_barplot(x, y, hue, data, ax=None, order=None):
    sns.barplot(x=x, y=y, hue=hue, ax=ax, order=order,
                data=(data[[x, hue]]
                      .reset_index(drop=True)
                      .groupby([x])[hue]
                      .value_counts(normalize=True)
                      .rename('Percentage').mul(100)
                      .reset_index()
                      .sort_values(hue)))
    ax.set_title("Percentage Normalized Occurrence of {} by {}".format(hue, x))
    ax.set_ylabel("Percentage %")

def create_wordcloud(df, word_list):
    word_freq = {}
    for index, row in df.iterrows():
        words = row['cleanedContent']
        for word in words:
            if word in word_list:
                word_freq[word] = word_freq.get(word, 0) + 1
    return WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

def plot_top_words(df, word_list, ax, color):
    word_counts = Counter()
    for index, row in df.iterrows():
        words = row['cleanedContent']
        for word in words:
            if word in word_list:
                word_counts[word] += 1
    words, counts = zip(*word_counts.most_common(20))
    ax.barh(range(len(words)), counts, align='center', color=color)
    ax.set_yticks(range(len(words)))
    ax.set_yticklabels(words)
    ax.set_xlabel('Số lần xuất hiện')

def calculate_sentiment_percentage(df):
    filtered_df = df[(df['brandName'] != 'None') & (df['Sentiment'].isin(['Positive', 'Negative']))]
    sentiment_counts = filtered_df.groupby(['brandName', 'Sentiment']).size().unstack().fillna(0)
    return sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100