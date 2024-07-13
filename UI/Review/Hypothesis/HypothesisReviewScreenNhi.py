import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt

from AppContext import AppContext
from String import StringManager
from DataManager.ReviewManager import ReviewManager

def hypothesisReviewScreenNhi(strings: StringManager):
    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("review_hypothesis_title")[0])

    # Lấy instance của ReviewManager
    review_manager = ReviewManager.get_instance()
        
    # Lấy dữ liệu
    df_new = review_manager.get_data()
    
    # Ghi tiêu đề
    st.markdown("## Trích xuất & phân tích những đặc điểm của sản phẩm thường được nhắc đến trong review")

    product_features = {
        'chất lượng': ['chất lượng', 'bền', 'đáng tin cậy', 'kém', 'chất', 'tốt', 'ổn', 'ok', 'oke', 'ổn định', 'good', 'nét', 'sắc nét', 'ngon', 'ngon lành', 'tạm', 'chắc chắn'],
        'giá cả': ['giá', 'chi phí', 'đắt', 'rẻ', 'tầm giá', 'giá cả', 'tiền', 'giá rẻ', 'giá tiền', 'giá trị', 'phải chăng', 'giảm giá', 'giá thành', 'đáng giá', 'tiết kiệm'],
        'thiết kế': ['thiết kế', 'phong cách', 'ngoại hình', 'đẹp', 'máy đẹp', 'hàng đẹp', 'mỏng', 'nhẹ', 'gọn', 'sang', 'sang trọng', 'hình thức', 'mẫu mã', 'chất liệu', 'bề ngoài', 'giao diện'],
        'hiệu năng': ['hiệu năng', 'tốc độ', 'hiệu quả', 'nhanh', 'nhạy', 'êm', 'mượt', 'mượt mà', 'sài mượt','mạnh', 'mạnh mẽ', 'hiệu suất', 'chậm', 'thời lượng', 'nóng', 'trâu', 'tệ', 'lag', 'treo', 'giật'],
        'đặc điểm kỹ thuật': ['pin', 'pin trâu', 'pin tốt', 'màn', 'màn hình', 'cấu hình', 'cảm ứng', 'camera', 'âm thanh', 'bộ nhớ', 'lưu trữ', 'màu', 'màu sắc', 'phim', 'quay phim', 'chụp', 'loa', 'sim', 'dung lượng', 'sạc', 'ram', 'phân giải','gọi', 'ứng dụng', 'tính năng', 'phần mềm', 'mạng', 'wifi' ],
        'dịch vụ': ['giao hàng', 'giao', 'đóng gói', 'dịch vụ', 'hậu mãi', 'bảo hành', 'đổi trả', 'đổi', 'nhiệt tình', 'tư vấn', 'hỗ trợ', 'phản hồi', 'chu đáo', 'cẩn thận', 'nhanh chóng', 'tặng', 'tặng kèm', 'thái độ', 'thân thiện', 'phục vụ', 'trả lời', 'vận chuyển', 'tận tình', 'miễn phí', 'có tâm'],
        'tình trạng sản phẩm': ['mới', 'cũ', 'seal', 'nguyên seal', 'hư', 'hư hỏng', 'mới tinh', 'mới cáo', 'lỗi', 'zin', 'nguyên zin', 'trầy', 'xước', 'trầy xước', 'nguyên', 'tình trạng']
    }

    word_counts = count_words(df_new['cleanedContent'])
    word_counts_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])
    word_counts_df = word_counts_df.sort_values(by='Count', ascending=False)
    word_counts_df = word_counts_df[word_counts_df['Count'] > 1]

    filtered_words_df = filter_words_by_features(word_counts_df, product_features)

    features = defaultdict(dict)
    for index, row in filtered_words_df.iterrows():
        feature = row['Feature']
        word = row['Word']
        count = row['Count']
        if word in features[feature]:
            features[feature][word] += count
        else:
            features[feature][word] = count

    word_counts = defaultdict(int)
    for index, row in filtered_words_df.iterrows():
        word = row['Word']
        count = row['Count']
        word_counts[word] += count

    # Visualization 1: Word Clouds cho từng đặc điểm và tổng hợp
    wordcloud_all = WordCloud(width=800, height=600, background_color='white', colormap='plasma').generate_from_frequencies(word_counts)
    fig, axs = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Word Clouds cho từng đặc điểm và tổng hợp')

    for i, (feature, words) in enumerate(features.items()):
        wordcloud = WordCloud(width=400, height=300, background_color='white', colormap='viridis').generate_from_frequencies(dict(words))
        axs[i//4, i%4].imshow(wordcloud, interpolation='bilinear')
        axs[i//4, i%4].set_title(feature)
        axs[i//4, i%4].axis('off')

    axs[1, 3].imshow(wordcloud_all, interpolation='bilinear')
    axs[1, 3].set_title('Tổng hợp')
    axs[1, 3].axis('off')

    st.pyplot(fig)
    st.markdown("""
        **Nhận xét:**
        """)
    
    # Visualization 2: Biểu đồ cột tổng Count cho mỗi Feature
    feature_totals = filtered_words_df.groupby('Feature')['Count'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(feature_totals['Feature'], feature_totals['Count'], color='skyblue')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')

    plt.title('Tổng Count cho mỗi Feature')
    plt.xlabel('Feature')
    plt.ylabel('Tổng Count')
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""
        **Nhận xét:**
        """)
    
    # Visualization 3: Biểu đồ cột Keywords Count by Brand and Feature
    for feature, keywords in product_features.items():
        df_new[feature + '_count'] = df_new['cleanedContent'].apply(lambda x: count_keywords(keywords, x))

    plot_data = pd.DataFrame()

    for feature, keywords in product_features.items():
        temp_df = df_new.groupby('brandName')[feature + '_count'].sum().reset_index()
        temp_df['Feature'] = feature.capitalize()
        temp_df.rename(columns={feature + '_count': 'Keywords Count'}, inplace=True)
        plot_data = pd.concat([plot_data, temp_df])

    plot_data.reset_index(drop=True, inplace=True)
    fig, ax = plt.subplots(figsize=(24, 12))
    sns.barplot(x='brandName', y='Keywords Count', hue='Feature', data=plot_data, alpha=0.8, ax=ax)
    plt.title('Keywords Count by Brand and Feature')
    plt.xlabel('Brand Name')
    plt.ylabel('Keywords Count')
    plt.ylim(0, 2000)
    plt.grid(axis='y')
    st.pyplot(fig)
    st.markdown("""
        **Nhận xét:**
        """)
    
    # Visualization 4: Biểu đồ tròn tỷ lệ đặc tính cho các brand hàng đầu
    top_brands = df_new['brandName'].value_counts().nlargest(6).index.tolist()
    df_top = df_new[df_new['brandName'].isin(top_brands)]

    feature_columns = ['chất lượng_count', 'giá cả_count', 'thiết kế_count', 'hiệu năng_count', 'đặc điểm kỹ thuật_count', 'dịch vụ_count', 'tình trạng sản phẩm_count']
    df_feature_counts = df_top.groupby('brandName')[feature_columns].sum()
    df_feature_counts.columns = ['chất lượng', 'giá cả', 'thiết kế', 'hiệu năng', 'đặc điểm kỹ thuật', 'dịch vụ', 'tình trạng sản phẩm']

    df_feature_counts['tổng giá trị'] = df_feature_counts.sum(axis=1)
    df_feature_counts = df_feature_counts.sort_values(by='tổng giá trị', ascending=False)
    df_feature_counts = df_feature_counts.drop(columns=['tổng giá trị'])
   
    fig, axs = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Biểu đồ tỷ lệ đặc tính cho các brand hàng đầu')
    colors = plt.cm.Set2.colors

    for i, brand in enumerate(df_feature_counts.index):
        sizes = df_feature_counts.loc[brand].values
        labels = df_feature_counts.columns
        axs[i//3, i%3].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        axs[i//3, i%3].set_title(f'Biểu đồ tỷ lệ của {brand}')

    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""
        **Nhận xét:**
        """)

    # Visualization 5: Biểu đồ cột tỷ lệ nhắc đến các đặc tính trong mỗi bình luận của các brand name
    df_binary = df_top[['brandName', 'chất lượng_count', 'giá cả_count', 'thiết kế_count', 'hiệu năng_count', 'đặc điểm kỹ thuật_count', 'dịch vụ_count', 'tình trạng sản phẩm_count']]
    df_binary.columns = ['brandName', 'chất lượng', 'giá cả', 'thiết kế', 'hiệu năng', 'đặc điểm kỹ thuật', 'dịch vụ', 'tình trạng sản phẩm']
    feature_columns = df_binary.columns[1:]
    
    for col in feature_columns:
        df_binary[col] = df_binary[col].apply(lambda x: 1 if x > 0 else 0)

    brand_feature_counts = df_binary.groupby('brandName').sum()
    brand_comment_counts = df_binary.groupby('brandName').size()
    brand_feature_ratios = brand_feature_counts.div(brand_comment_counts, axis=0)

    plot_data = brand_feature_ratios.reset_index().melt(id_vars='brandName', var_name='Feature', value_name='Ratio')  
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x='brandName', y='Ratio', hue='Feature', data=plot_data, alpha=0.8)
    plt.title('Tỷ lệ nhắc đến các đặc tính trong mỗi bình luận của các brand name')
    plt.xlabel('Brand Name')
    plt.ylabel('Tỷ lệ nhắc đến')
    plt.legend(title='Đặc tính')
    plt.grid(axis='y')
    st.pyplot(fig)

    st.markdown("""
        **Nhận xét:**
        """)
    
    appContext = AppContext.get_instance()
    appContext.titlePage = strings.get_string("review_hypothesis_title")[0]
    appContext.content = "Đây là trích xuất & phân tích những đặc điểm của sản phẩm thường được nhắc đến trong review"
    appContext.hyphothesisTitle = "Từ đây ta đưa ra dược các nhận xét như sau"

    # hpsContent sẽ là kết quả của phân tích
    # hpsContent = (f"Kết quả mô hình OLS: \n {model.summary().as_text()} \n "
    #               f"\n Kết luận: \n{conclusions}")
    # appContext.hyphothesisContent = hpsContent

# Các hàm hỗ trợ
def count_words(content_column):
    word_counts = Counter()
    for content in content_column:
        word_counts.update(content)
    return word_counts

@st.cache_data
def filter_words_by_features(word_counts_df, features_dict):
    result = pd.DataFrame(columns=['Feature', 'Word', 'Count'])
    for feature, keywords in features_dict.items():
        filtered_words = word_counts_df[word_counts_df['Word'].isin(keywords)]
        filtered_words['Feature'] = feature
        result = pd.concat([result, filtered_words], ignore_index=True)
    return result

@st.cache_data
def count_keywords(keywords, text):
    count = sum(1 for word in text if word in keywords)
    return count

