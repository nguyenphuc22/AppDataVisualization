import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt

from AppContext import AppContext
from String import StringManager
from DataManager.ReviewManager import ReviewManager
from ChatBot import OpenAIChatbot


def hypothesisReviewScreenNhi(strings: StringManager):
    print("Hypothesis Review Screen Nhi Entry")
    st.title(strings.get_string("review_hypothesis_title")[0])
    st.markdown("## Trích xuất & phân tích những đặc điểm của sản phẩm thường được nhắc đến trong review")

    # Load data
    review_manager = ReviewManager.get_instance()
    df_new = review_manager.get_data()

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

    filtered_words_dict = filter_words_by_features(word_counts_df, product_features)

    # Flatten the dictionary for the overall word counts
    overall_word_counts = sum((Counter(words) for words in filtered_words_dict.values()), Counter())

    # Visualization 1: Word Clouds cho từng đặc điểm và tổng hợp
    st.subheader('1. Mô hình đám mây từ cho các từ khóa đánh giá sản phẩm')
    wordcloud_all = WordCloud(width=800, height=600, background_color='white', colormap='plasma').generate_from_frequencies(overall_word_counts)
    
    fig, axs = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Word Clouds cho từng đặc điểm và tổng hợp')

    for i, (feature, words) in enumerate(filtered_words_dict.items()):
        wordcloud = WordCloud(width=400, height=300, background_color='white', colormap='viridis').generate_from_frequencies(words)
        axs[i // 4, i % 4].imshow(wordcloud, interpolation='bilinear')
        axs[i // 4, i % 4].set_title(feature)
        axs[i // 4, i % 4].axis('off')

    axs[1, 3].imshow(wordcloud_all, interpolation='bilinear')
    axs[1, 3].set_title('Tổng hợp')
    axs[1, 3].axis('off')

    st.pyplot(fig)
    
    # Visualization 2: Biểu đồ cột tổng Count cho mỗi Feature
    st.subheader('2. Biểu đồ cột biểu diễn tổng số lần xuất hiện của các nhóm từ khóa đánh giá sản phẩm')
    # Convert `filtered_words_dict` to a DataFrame for plotting
    data = {
        'Feature': [],
        'Count': []
    }
    for feature, words in filtered_words_dict.items():
        total_count = sum(words.values())
        data['Feature'].append(feature)
        data['Count'].append(total_count)

    feature_totals = pd.DataFrame(data)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(feature_totals['Feature'], feature_totals['Count'], color='skyblue')

    # Add text labels on the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

    # Customize plot
    plt.title('Tổng Count cho mỗi Feature')
    plt.xlabel('Feature')
    plt.ylabel('Tổng Count')
    plt.xticks(rotation=30)
    plt.tight_layout()

    # Display plot
    st.pyplot(fig)

    # Analyzing the top features
    top_features = feature_totals.sort_values(by='Count', ascending=False).reset_index(drop=True)
    top_feature_names = top_features['Feature'].tolist()
    top_counts = top_features['Count'].tolist()

    # Extract top 4 features and their counts
    top_details = [(top_feature_names[i] if i < len(top_feature_names) else "không đủ dữ liệu",
                    top_counts[i] if i < len(top_counts) else 0) 
                for i in range(4)]

    # Format the comment
    content2 = f"""Thông qua Biểu đồ cột biểu diễn tổng số lần xuất hiện của các nhóm từ khóa đánh giá sản phẩm, rút ra được một số kết luận về sự quan tâm của các khách hàng như sau:

    - Nhóm từ khóa '{top_details[0][0]}' có tổng số lần xuất hiện cao nhất, với {int(top_details[0][1])} lượt, cho thấy đây là yếu tố quan trọng nhất đối với khách hàng khi mua sắm sản phẩm điện tử.

    - Tiếp theo là nhóm từ khóa '{top_details[1][0]}' với {int(top_details[1][1])} lượt, cho thấy sự quan tâm lớn của khách hàng đến yếu tố này.

    - Nhóm từ khóa '{top_details[2][0]}' và '{top_details[3][0]}' lần lượt đứng thứ ba và thứ tư, với {int(top_details[2][1])} và {int(top_details[3][1])} lượt xuất hiện, cho thấy các yếu tố này cũng được khách hàng quan tâm nhưng không nhiều bằng hai yếu tố chính.
    """

    # Display the content
    st.write(content2)
    
    # Visualization 3: Biểu đồ cột Keywords Count by Brand and Feature
    st.subheader('3. Biểu đồ cột biểu diễn tổng số lượng mỗi nhóm từ khóa cho từng nhãn hàng')
    # for feature, keywords in product_features.items():
    #     df_new[feature + '_count'] = df_new['cleanedContent'].apply(lambda x: count_keywords(keywords, x))
    for feature, keywords in product_features.items():
        df_new[feature + '_count'] = count_keywords_optimized(keywords, df_new['cleanedContent'])

    plot_data_list = []
    for feature in product_features.keys():
        temp_df = df_new.groupby('brandName')[feature + '_count'].sum().reset_index()
        temp_df['Feature'] = feature.capitalize()
        temp_df.rename(columns={feature + '_count': 'Keywords Count'}, inplace=True)
        plot_data_list.append(temp_df)

    plot_data = pd.concat(plot_data_list, ignore_index=True)

    # Find the maximum value for the y-axis
    max_y = plot_data['Keywords Count'].max()

    # Plotting
    fig, ax = plt.subplots(figsize=(24, 12))
    sns.barplot(x='brandName', y='Keywords Count', hue='Feature', data=plot_data, alpha=0.8, ax=ax)
    plt.title('Keywords Count by Brand and Feature')
    plt.xlabel('Brand Name')
    plt.ylabel('Keywords Count')
    plt.ylim(0, max_y + max_y * 0.1)  # Adding 10% margin to the max value
    plt.grid(axis='y')
    st.pyplot(fig)

    # Nhận xét động trực quan 3
    # Tính toán các thông số cần thiết
    # Analyzing top brands and features more efficiently
    top_brands = plot_data.groupby('brandName', as_index=False)['Keywords Count'].sum().nlargest(3, 'Keywords Count')
    top_features = plot_data.groupby('Feature', as_index=False)['Keywords Count'].sum().nlargest(3, 'Keywords Count')

    # Extract top brands and counts
    top_brands_names = top_brands['brandName'].tolist()
    top_brands_counts = top_brands['Keywords Count'].tolist()

    top_brand1, top_brand2, top_brand3 = (top_brands_names + ["không đủ dữ liệu"] * 3)[:3]
    top_brand1_count, top_brand2_count, top_brand3_count = (top_brands_counts + [0] * 3)[:3]

    # Extract top features and counts
    top_feature_names = top_features['Feature'].tolist()
    top_feature_counts = top_features['Keywords Count'].tolist()

    top_feature1, top_feature2, top_feature3 = (top_feature_names + ["không đủ dữ liệu"] * 3)[:3]
    top_feature1_count, top_feature2_count, top_feature3_count = (top_feature_counts + [0] * 3)[:3]

    # Format comments
    content3 = f"""Thông qua biểu đồ Biểu đồ cột biểu diễn tổng số lượng mỗi nhóm từ khóa cho từng nhãn hàng, rút ra được một số kết luận về sự quan tâm của khách hàng như sau:

    - Thương hiệu '{top_brand1}' dẫn đầu với tổng số {int(top_brand1_count)} lượt xuất hiện các từ khóa, cho thấy đây là nhãn hàng nhận được nhiều sự quan tâm nhất.

    - Tiếp theo là các thương hiệu '{top_brand2}' và '{top_brand3}' với tổng số lượt xuất hiện lần lượt là {int(top_brand2_count)} và {int(top_brand3_count)} lượt, cho thấy sự quan tâm lớn đến các nhãn hàng này.

    - Các nhóm từ khóa chính mà khách hàng quan tâm bao gồm '{top_feature1}' với tổng số {int(top_feature1_count)} lượt, '{top_feature2}' và '{top_feature3}' cũng thu hút sự chú ý lớn, cho thấy sự quan tâm chủ yếu đến các yếu tố này.
    """
    
    # Visualization 4: Biểu đồ tròn tỷ lệ đặc tính cho các brand hàng đầu
    st.subheader('4. Biểu đồ tròn biểu diễn tỷ lệ giữa các nhóm từ khóa cho từng nhãn hàng')
    top_brands = df_new['brandName'].value_counts().nlargest(3).index
    df_top = df_new[df_new['brandName'].isin(top_brands)]
    feature_columns = [
        'chất lượng_count', 'giá cả_count', 'thiết kế_count',
        'hiệu năng_count', 'đặc điểm kỹ thuật_count',
        'dịch vụ_count', 'tình trạng sản phẩm_count'
    ]
    df_feature_counts = df_top.groupby('brandName')[feature_columns].sum()
    df_feature_counts.columns = [
        'chất lượng', 'giá cả', 'thiết kế', 'hiệu năng',
        'đặc điểm kỹ thuật', 'dịch vụ', 'tình trạng sản phẩm'
    ]
    df_feature_counts['tổng giá trị'] = df_feature_counts.sum(axis=1)
    df_feature_counts = df_feature_counts.sort_values(by='tổng giá trị', ascending=False).drop(columns=['tổng giá trị'])
   

    fig, axs = plt.subplots(1, 3, figsize=(20, 6))  # Tạo một hàng với 3 biểu đồ
    fig.suptitle('Biểu đồ tỷ lệ đặc tính cho các brand hàng đầu')
    colors = plt.cm.Set2.colors

    for i, brand in enumerate(df_feature_counts.index[:3]):  # Chỉ lấy 3 brand đầu tiên
        sizes = df_feature_counts.loc[brand].values
        labels = df_feature_counts.columns
        axs[i].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        axs[i].set_title(f'Biểu đồ tỷ lệ của {brand}')
        plt.tight_layout()

    st.pyplot(fig)

    # Nhận xét động trực quan 4
    # Tính toán các tỷ lệ phần trăm và sự chênh lệch
    # Find top brand and top feature for that brand
    top_brand = df_feature_counts.index[0]
    top_feature = df_feature_counts.loc[top_brand].idxmax()
    top_feature_percentage = df_feature_counts.loc[top_brand].max() / df_feature_counts.loc[top_brand].sum() * 100

    # Select top 3 brands
    top_brands = df_feature_counts.index[:3]

    # Initialize dictionary to store results
    brand_features = {}

    # Calculate top features and their percentages for each top brand
    for brand in top_brands:
        top_feature = df_feature_counts.loc[brand].idxmax()
        second_top_feature = df_feature_counts.loc[brand].nlargest(2).index[1]
        diff = df_feature_counts.loc[brand, top_feature] - df_feature_counts.loc[brand, second_top_feature]
        diff_percentage = diff / df_feature_counts.loc[brand].sum() * 100
        brand_features[brand] = {
            'top_feature': top_feature,
            'second_top_feature': second_top_feature,
            'diff_percentage': diff_percentage
        }

    # Extract brand data for the top 3 brands
    brand_1 = top_brands[0]
    brand_2 = top_brands[1]
    brand_3 = top_brands[2]

    brand_1_data = brand_features[brand_1]
    brand_2_data = brand_features[brand_2]
    brand_3_data = brand_features[brand_3]

    content4 = f""" Thông qua Biểu đồ tròn biểu diễn tỷ lệ giữa các nhóm từ khóa cho từng nhãn hàng, rút ra được một số kết luận về sự quan tâm của khách hàng như sau:

    - '{top_feature}' luôn là đặc điểm được quan tâm nhiều nhất với tỷ lệ vượt trội trên {top_feature_percentage:.1f}% so với toàn bộ các từ khóa.

    - Các khách hàng của nhãn hàng {brand_1} nhắc nhiều về các từ khóa '{brand_1_data['top_feature']}' hơn '{brand_1_data['second_top_feature']}', với sự chênh lệch xấp xỉ {brand_1_data['diff_percentage']:.1f}%.
        
    - Các khách hàng của {brand_2} nhắc đến nhiều về các đặc điểm '{brand_2_data['top_feature']}' hơn, mà trong đó sự chênh lệch giữa hai đặc điểm này ở {brand_2} là {brand_2_data['diff_percentage']:.1f}%.
        
    - Tiếp theo khách hàng của {brand_3} nhắc đến nhiều về các đặc điểm '{brand_3_data['top_feature']}' hơn, mà trong đó sự chênh lệch giữa hai đặc điểm này ở {brand_3} là {brand_3_data['diff_percentage']:.1f}%.
    """


    # Visualization 5: Biểu đồ cột tỷ lệ nhắc đến các đặc tính trong mỗi bình luận của các brand name
    st.subheader('5. Biểu đồ biểu diễn xác suất xuất hiện từ khóa trong mỗi bình luận cho từng nhãn hàng')
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
    plt.xlabel('Hãng sản phảm')
    plt.ylabel('Tỷ lệ nhắc đến')
    plt.legend(title='Đặc tính')
    plt.grid(axis='y')
    st.pyplot(fig)

    # Nhận xét động hình ảnh trực quan 5
    # Tìm các nhãn hàng và đặc tính được nhắc đến nhiều nhất
    top_features = brand_feature_ratios.max().sort_values(ascending=False).index[:4]
    top_features_brands = {feature: brand_feature_ratios[feature].idxmax() for feature in top_features}
    top_features_ratios = {feature: brand_feature_ratios[feature].max() * 100 for feature in top_features}

    # Lấy nhãn hàng và tỷ lệ cho các đặc tính khác
    second_highest_ratios = {
        feature: brand_feature_ratios[feature].nlargest(2).values[1] * 100 for feature in top_features
    }
    second_highest_brands = {
        feature: brand_feature_ratios[feature].nlargest(2).index[1] for feature in top_features
    }

    content5 = f""" Thông qua Biểu đồ biểu diễn xác suất xuất hiện từ khóa trong mỗi bình luận cho từng nhãn hàng, rút ra được một số kết luận về sự quan tâm của khách hàng như sau:

    - '{top_features[0]}': {top_features_brands[top_features[0]]} và {second_highest_brands[top_features[0]]} có tỷ lệ nhắc đến '{top_features[0]}' cao nhất, cho thấy người tiêu dùng rất chú trọng đến {top_features[0]} khi đánh giá các sản phẩm của hai nhãn hiệu này, với tỷ lệ lần lượt là {top_features_ratios[top_features[0]]:.1f}% và {second_highest_ratios[top_features[0]]:.1f}%.
        
    - '{top_features[1]}': {top_features_brands[top_features[1]]} có tỷ lệ nhắc đến '{top_features[1]}' cao hơn so với các nhãn hàng khác, cho thấy người tiêu dùng rất quan tâm đến '{top_features[1]}' của sản phẩm {top_features_brands[top_features[1]]}, với tỷ lệ là {top_features_ratios[top_features[1]]:.1f}%.
        
    - '{top_features[2]}': '{top_features[2]}' được nhắc đến nhiều ở {top_features_brands[top_features[2]]}, cho thấy sự quan tâm lớn đến '{top_features[2]}' của sản phẩm từ nhãn hiệu này, với tỷ lệ là {top_features_ratios[top_features[2]]:.1f}%.
        
    - '{top_features[3]}': Tỷ lệ nhắc đến '{top_features[3]}' khá cao ở {top_features_brands[top_features[3]]} và {second_highest_brands[top_features[3]]}, cho thấy '{top_features[3]}' là một yếu tố quan trọng trong các đánh giá của người tiêu dùng, với tỷ lệ lần lượt là {top_features_ratios[top_features[3]]:.1f}% và {second_highest_ratios[top_features[3]]:.1f}%.
    """
    # st.markdown(f""" **Nhận xét:**
                
    #             {content5}""")
    
    openAi = OpenAIChatbot()
    appContext = AppContext.get_instance()
    appContext.titlePage = strings.get_string("review_hypothesis_title")[0]
    appContext.content = "Đây là trích xuất & phân tích những đặc điểm của sản phẩm thường được nhắc đến trong review"
    appContext.hyphothesisTitle = "Trích xuất & phân tích những đặc điểm của sản phẩm thường được nhắc đến trong review"

    # hpsContent sẽ là kết quả của phân tích
    hpsContent = (f"""
    1. Hình ảnh trực quan 1: Mô hình đám mây từ cho các từ khóa đánh giá sản phẩm
                  
    2. Hình ảnh trực quan 2:
    {content2}

    3. Hình ảnh trực quan 3:
    {content3}

    4. Hình ảnh trực quan 4:
    {content4}

    5. Hình ảnh trực quan 5:
    {content5}
    """)
    appContext.hyphothesisContent = hpsContent
    appContext.prompt = "Dựa vào giả thuyết đặc điểm của sản phẩm thường được nhắc đến trong review trên hãy nhận xét cho tôi dạng markdown"
    response = openAi.generate_response(appContext) 

    st.markdown(response)

# Các hàm hỗ trợ
@st.cache_data
def count_words(content_column):
    return Counter(word for content in content_column for word in content)

@st.cache_data
def filter_words_by_features(word_counts_df, features_dict):
    """Filter words by features and their keywords."""
    filtered_words_dict = {}
    for feature, keywords in features_dict.items():
        filtered_df = word_counts_df[word_counts_df['Word'].isin(keywords)]
        filtered_words_dict[feature] = dict(zip(filtered_df['Word'], filtered_df['Count']))
    return filtered_words_dict

@st.cache_data
def count_keywords_optimized(keywords, df_col):
    keywords_set = set(keywords)
    return df_col.apply(lambda x: sum(word in keywords_set for word in x))