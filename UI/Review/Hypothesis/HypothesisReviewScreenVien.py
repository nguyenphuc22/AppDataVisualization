import streamlit as st
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

from AppContext import AppContext
from FixedContent import FixedContent
from String import StringManager
from DataManager.ReviewManager import ReviewManager
from ChatBot import OpenAIChatbot

def hypothesisReviewScreenVien(strings: StringManager):
    print("Hypothesis Review Screen Vien Entry")
    st.title(strings.get_string("review_hypothesis_title")[1])
    # st.title(strings.get_string("hypothesis_title"))
    # st.write(strings.get_string("review_hypothesis_title")[1])

    # Lấy instance của ReviewManager
    review_manager = ReviewManager.get_instance()

    # Lấy dữ liệu
    df_new = review_manager.get_data()

    # Ghi tiêu đề
    st.markdown("## Phân tích dữ liệu dựa trên cảm xúc của người dùng tác động như thế nào đánh chỉ số đánh giá và các nhãn hàng lớn trên thế giới") 

    # Hiển thị tóm tắt dữ liệu
    # st.write(review_manager.get_data_summary())

    # Visualization 1: Cảm xúc tổng thể
    st.subheader("1. Các cảm xúc tổng thể")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x="Sentiment", data=df_new, ax=ax, order=["Negative", "Neutral", "Positive"], palette="viridis")
    ax.set_xlabel("Cảm xúc", fontsize=12)
    ax.set_ylabel("Số lượng", fontsize=12)
    plt.savefig('ChatBotUtils/image/reviews_sentiment_general.png')
    st.pyplot(fig)

    # Thêm nhận xét động cho trực quan 1
    sentiment_counts = df_new['Sentiment'].value_counts()
    negative_count = sentiment_counts.get("Negative", 0)
    neutral_count = sentiment_counts.get("Neutral", 0)
    positive_count = sentiment_counts.get("Positive", 0)

    content1 = f"""Cảm xúc tiêu cực chiếm khoảng {negative_count} lượt trong dữ liệu, tương ứng với các cảm xúc trung lập và tích cực lần lượt là vào khoảng {neutral_count} lượt và {positive_count} lượt.
    """
    # st.markdown(f""" **Nhận xét:**
                
    #             {content1} """)

    # Visualization 2: Đánh giá tổng thể
    st.subheader("2. Các đánh giá tổng thể")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x="rating", data=df_new, ax=ax, palette="viridis")
    ax.set_xlabel("Đánh giá", fontsize=12)
    ax.set_ylabel("Số lượng", fontsize=12)
    plt.savefig('ChatBotUtils/image/reviews_rating_general.png')
    st.pyplot(fig)

    # Thêm nhận xét động cho trực quan 2
    # Tính toán số lượng các đánh giá
    rating_counts = df_new['rating'].value_counts().sort_index()

    # Tính số lượng đánh giá cao và thấp
    high_ratings = rating_counts.loc[rating_counts.index >= 4].sum()
    low_ratings = rating_counts.loc[rating_counts.index <= 2].sum()
    
    if high_ratings > low_ratings:
        content2 = f"Đa số khách hàng đánh giá rất cao sản phẩm và dịch vụ, với {high_ratings} đánh giá từ 4 sao trở lên, cho thấy được sự hài lòng cao. Tuy nhiên ta cần tìm hiểu thêm các lý do tại sao vẫn có {low_ratings} đánh giá thấp."
    else:
        content2 = f"Đa số khách hàng đánh giá không cao sản phẩm và dịch vụ, với khoảng {low_ratings} đánh giá từ 2 sao trở xuống, cho thấy được sự hài lòng không cao. Ta cần phải tìm hiểu tại sao lại đánh giá thấp."
    # st.markdown(f""" **Nhận xét:**
                
    #             {content2}  """)

    # Visualization 3: Tần suất đánh giá theo cảm xúc
    st.subheader("3. Tần suất đánh giá (%) theo cảm xúc")
    fig, ax = plt.subplots(figsize=(12, 8))
    percentstandardize_barplot(x="rating", y="Percentage", hue="Sentiment", data=df_new, ax=ax)
    ax.set_xlabel("Đánh giá")
    ax.set_ylabel("Phần trăm %")
    plt.savefig('ChatBotUtils/image/reviews_sentimentVsRating_percentage.png')
    st.pyplot(fig)

    # Thêm nhận xét động như trực quan 3
    # Tính toán tỷ lệ phần trăm của các cảm xúc theo từng mức rating
    rating_sentiment_counts = df_new.groupby('rating')['Sentiment'].value_counts(normalize=True).mul(100).unstack()

    # Lấy các giá trị phần trăm
    negative_1_star = rating_sentiment_counts.loc[1, 'Negative'] if 'Negative' in rating_sentiment_counts.columns else 0
    neutral_1_star = rating_sentiment_counts.loc[1, 'Neutral'] if 'Neutral' in rating_sentiment_counts.columns else 0
    positive_1_star = rating_sentiment_counts.loc[1, 'Positive'] if 'Positive' in rating_sentiment_counts.columns else 0

    negative_5_star = rating_sentiment_counts.loc[5, 'Negative'] if 'Negative' in rating_sentiment_counts.columns else 0
    neutral_5_star = rating_sentiment_counts.loc[5, 'Neutral'] if 'Neutral' in rating_sentiment_counts.columns else 0
    positive_5_star = rating_sentiment_counts.loc[5, 'Positive'] if 'Positive' in rating_sentiment_counts.columns else 0

    # Nhận xét động với điều kiện if-elif-else
    if positive_1_star != 0 and negative_5_star != 0:
        content3 = f"Biểu đồ tần suất đánh giá % theo cảm xúc cho thấy rằng đánh giá 1 sao chủ yếu là tiêu cực (khoảng {negative_1_star:.1f}%), trung lập (khoảng {neutral_1_star:.1f}%) và tích cực (khoảng {positive_1_star:.1f}%). Đánh giá 5 sao có cả tiêu cực (khoảng {negative_5_star:.1f}%), trung lập (khoảng {neutral_5_star:.1f}%) và tích cực (khoảng {positive_5_star:.1f}%). Một số lý do có thể giải thích cảm xúc tích cực trong đánh giá 1 sao bao gồm đánh giá dựa trên một khía cạnh cụ thể, sự thất vọng và việc gửi thông điệp mạnh mẽ. Ngược lại, phản hồi tiêu cực trong đánh giá 5 sao có thể do tiêu chuẩn đánh giá khác nhau, cân nhắc tổng thể, tâm lý “mềm lòng,” sự trung thành với thương hiệu và mong muốn khuyến khích cải thiện."
    elif positive_1_star == 0 and negative_5_star == 0:
        content3 = f"Biểu đồ tần suất đánh giá % theo cảm xúc cho thấy rằng cảm xúc tiêu cực chiếm trong đánh giá 1 sao khoảng {negative_1_star:.1f}% lượt trong dữ liệu, cảm xúc tích cực trong đánh giá 5 sao chiếm khoảng {positive_5_star:.1f}%. Điều này cho ta thấy rằng các đánh giá tiêu cực chủ yếu đi kèm với cảm xúc tiêu cực, trong khi đánh giá cao (4-5 sao) chủ yếu đi kèm với cảm xúc tích cực. Điều này xác nhận rằng cảm xúc tích cực thường dẫn đến đánh giá cao và ngược lại."
    elif positive_1_star != 0 and negative_5_star == 0:
        content3 = f"Biểu đồ tần suất đánh giá % theo cảm xúc cho thấy rằng cảm xúc tiêu cực và tích cực chiếm trong đánh giá 1 sao lần lượt khoảng {negative_1_star:.1f}% và {positive_1_star:.1f}% trong dữ liệu, cảm xúc tích cực trong đánh giá 5 sao chiếm khoảng {positive_5_star:.1f}%. Điều này cho ta thấy rằng các đánh giá tiêu cực chủ yếu đi kèm với cảm xúc tiêu cực, trong khi đánh giá cao (4-5 sao) chủ yếu đi kèm với cảm xúc tích cực. Điều này xác nhận rằng cảm xúc tích cực thường dẫn đến đánh giá cao và ngược lại. Một số lý do có thể giải thích cảm xúc tích cực trong đánh giá 1 sao bao gồm đánh giá dựa trên một khía cạnh cụ thể, sự thất vọng và việc gửi thông điệp mạnh mẽ."
    else:
        content3 = f"Biểu đồ tần suất đánh giá % theo cảm xúc cho thấy rằng cảm xúc tiêu cực chiếm trong đánh giá 1 sao khoảng {negative_1_star:.1f}% trong dữ liệu, cảm xúc tích cực và tiêu cực trong đánh giá 5 sao chiếm lần lượt khoảng {positive_5_star:.1f}% và {neutral_5_star:.1f}%. Điều này cho ta thấy rằng các đánh giá tiêu cực chủ yếu đi kèm với cảm xúc tiêu cực, trong khi đánh giá cao (4-5 sao) chủ yếu đi kèm với cảm xúc tích cực. Điều này xác nhận rằng cảm xúc tích cực thường dẫn đến đánh giá cao và ngược lại. Một số lý do có thể giải thích cảm xúc tiêu cực trong đánh giá 5 sao bao gồm tiêu chuẩn đánh giá khác nhau, cân nhắc tổng thể, tâm lý “mềm lòng,” sự trung thành với thương hiệu và mong muốn khuyến khích cải thiện."
    # st.markdown(f""" **Nhận xét:**
                
    #             {content3}""")

    # Visualizatin 4: Word Clouds và Top Words
    st.subheader("4. Phân tích từ ngữ")
    col1, col2 = st.columns(2)

    def get_top_words(word_list, num_words=20):
        word_counter = Counter(word_list)
        return [word for word, count in word_counter.most_common(num_words)]

    with col1:
        st.write("Các từ xuất hiện nhiều với cảm xúc tích cực")
        positive_wordcloud = create_wordcloud(df_new, review_manager.positive_words)
        st.image(positive_wordcloud.to_array())

        st.write("Top 20 từ tích cực")
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_top_words(df_new, review_manager.positive_words, ax, color='green')
        st.pyplot(fig)

        # Lấy top 20 từ tích cực
        top_positive_words = get_top_words(review_manager.positive_words)

    with col2:
        st.write("Các từ xuất hiện nhiều với cảm xúc tiêu cực")
        negative_wordcloud = create_wordcloud(df_new, review_manager.negative_words)
        st.image(negative_wordcloud.to_array())

        st.write("Top 20 từ tiêu cực")
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_top_words(df_new, review_manager.negative_words, ax, color='red')
        st.pyplot(fig)

        # Lấy top 20 từ tiêu cực
        top_negative_words = get_top_words(review_manager.negative_words)

    # Create plots for save
    fig, axs = plt.subplots(2, 2, figsize=(20, 12))
    axs[0, 0].imshow(positive_wordcloud, interpolation='bilinear')                  # Positive wordcloud
    axs[0, 0].set_title('Các từ xuất hiện nhiều với cảm xúc tích cực')
    axs[0, 0].axis('off')
    plot_top_words(df_new, review_manager.positive_words, axs[0, 1], color='green') # Positive top words    
    axs[1, 0].imshow(negative_wordcloud, interpolation='bilinear')                  # Negative wordcloud
    axs[1, 0].set_title('Các từ xuất hiện nhiều với cảm xúc tiêu cực')
    axs[1, 0].axis('off')
    plot_top_words(df_new, review_manager.negative_words, axs[1, 1], color='red')  # Negative top words
    # Save the combined figure as a PNG file
    plt.tight_layout()
    plt.savefig('ChatBotUtils/image/reviews_sentimentTopWords_wordcloud.png')

    positive_comments = [word for word in review_manager.positive_words if word in top_positive_words]
    negative_comments = [word for word in review_manager.negative_words if word in top_negative_words]

    if positive_comments:
        content4_positive = f"Các từ tích cực như: {', '.join(positive_comments)} cho thấy sản phẩm/dịch vụ đáp ứng tốt tiêu chuẩn và xây dựng niềm tin với khách hàng. Đồng thời là nhanh nhẹn và mới mẻ. Cho thấy sự hài lòng cao của khách hàng"
    if negative_comments:
        content4_negative = f"Các từ tiêu cực như: {', '.join(negative_comments)} phản ánh chất lượng sản phẩm và sự thất vọng về độ tin cậy và trung thực."
    content4 = f"""
    - {content4_positive}
    
    - {content4_negative}"""
    # st.markdown(f""" **Nhận xét**:
                
    #             {content4}""")

    # Visulisation 5: Phân tích cảm xúc theo thương hiệu
    st.subheader("5. Tỷ lệ phần trăm theo cảm xúc cho từng thương hiệu")
    sentiment_percent = calculate_sentiment_percentage(df_new)
    fig, ax = plt.subplots(figsize=(14, 10))
    sentiment_percent.plot(kind='bar', stacked=True, colormap='plasma', ax=ax, edgecolor='black')
    ax.set_xlabel('Thương hiệu')
    ax.set_ylabel('Tỷ lệ phần trăm (%)')
    plt.xticks(rotation=45)
    ax.legend(title='Sentiment', labels=['Negative', 'Positive'])
    plt.savefig('ChatBotUtils/image/reviews_sentimentVsBrands_percentage.png')
    st.pyplot(fig)


    # Thêm nhận xét động như trực quan 5
    # Tạo nhận xét động
    positive_sentiments = sentiment_percent['Positive'].dropna()
    negative_sentiments = sentiment_percent['Negative'].dropna()

    # So sánh tổng đánh giá tích cực và tiêu cực
    total_positive = positive_sentiments.sum()
    total_negative = negative_sentiments.sum()

    if total_positive > total_negative:
        content5_a = f"Tỷ lệ đánh giá tích cực lớn hơn so với tiêu cực."
    else:
        content5_a = f"Tỷ lệ đánh giá tiêu cực lớn hơn so với tích cực."

    # Tìm thương hiệu có đánh giá tích cực cao nhất
    top_positive_brands = positive_sentiments.sort_values(ascending=False).head(4)
    top1_positive_brand = top_positive_brands.index[0]
    top2_positive_brand = top_positive_brands.index[1]
    top3_positive_brand = top_positive_brands.index[2]
    top4_positive_brand = top_positive_brands.index[3]

    content5_b = f"Thương hiệu {top1_positive_brand} dẫn đầu ở mức {top_positive_brands.iloc[0]:.1f}%, tiếp theo là thương hiệu {top2_positive_brand} ở mức {top_positive_brands.iloc[1]:.1f}%, sau đó là {top3_positive_brand} và {top4_positive_brand} với tỷ lệ lần lượt là {top_positive_brands.iloc[2]:.1f}% và {top_positive_brands.iloc[3]:.1f}%."

    # Tìm thương hiệu có đánh giá tiêu cực cao nhất
    top_negative_brands = negative_sentiments.sort_values(ascending=False).head(2)
    top1_negative_brand = top_negative_brands.index[0]
    top2_negative_brand = top_negative_brands.index[1]

    content5_c = f"Thương hiệu {top1_negative_brand} và {top2_negative_brand} có điểm đánh giá tiêu cực cao nhất. Hãng đang đối mặt với một vài thách thức về hình ảnh và sự hài lòng của khách hàng."

    # Kiểm tra sự tồn tại đồng thời của Apple và Samsung
    if 'Apple' in sentiment_percent.index and 'Samsung' in sentiment_percent.index:
        apple_samsung_comment = f"2 thương hiệu lớn Apple và Samsung vẫn đang giữ vị thế vững chắc nhưng đang phải đối mặt cao sự kỳ vọng của người dùng."
    else:
        apple_samsung_comment = f""

    if apple_samsung_comment:
        content5 = f"""
    - {content5_a}

    - {content5_b}

    - {content5_c}

    - {apple_samsung_comment}"""
    else:
        content5 = f"""
    - {content5_a}

    - {content5_b}

    - {content5_c}"""
    # st.markdown(f"""**Nhận xét**: 
                
    #             {content5} """)

    # Cập nhật AppContext
    openAi = OpenAIChatbot()
    appContext = AppContext.get_instance()
    appContext.titlePage = strings.get_string("review_hypothesis_title")[1]
    appContext.content = "Đây là phần phân tích cảm xúc của người dùng có tác động như thế nào đến đánh giá và các nhãn hàng lớn trên thế giới."
    appContext.hyphothesisTitle = "Các yếu tố ảnh hưởng đến cảm xúc dựa trên rating và các thương hiệu"

    # hpsContent sẽ là kết quả của phân tích
    hpsContent = (f"""
    1. Hình ảnh trực quan 1: Cảm xúc tổng thể
    Nhận xét:             
    {content1}

    2. Hình ảnh trực quan 2: Đánh giá tổng thể
    Nhận xét: 
    {content2}

    3. Hình ảnh trực quan 3: Tần suất đánh giá theo cảm xúc
    Nhận xét: 
    {content3}

    4. Hình ảnh trực quan 4: Word Clouds và Top Words
    Nhận xét:     
    {content4}

    5. Hình ảnh trực quan 5: Phân tích cảm xúc theo thương hiệu
    Nhận xét:     
    {content5}
    """)
    appContext.hyphothesisContent = hpsContent
    appContext.prompt = "Hãy nhận xét giả thuyết phân tích cảm xúc của người dùng có tác động như thế nào đến đánh giá và các nhãn hàng lớn trên thế giới cho tôi dạng markdown"

    fixedContent = FixedContent.get_instance()
    fixedContent.reviews_sentiments_generalContent = hpsContent
    
    response = openAi.generate_response(appContext)
    st.markdown(f"<div style='color: cyan; text-align: right;'>{strings.get_string('you')}: {appContext.prompt}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: left;'>{strings.get_string('bot')}:\n\n {response}</div>", unsafe_allow_html=True)

# Các hàm hỗ trợ 
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
