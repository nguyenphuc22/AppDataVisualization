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
    # st.title(strings.get_string("hypothesis_title"))
    # st.write(strings.get_string("review_hypothesis_title")[0])

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
    st.subheader('1. Mô hình đám mây từ cho các từ khóa đánh giá sản phẩm')
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
    # st.markdown("""
    #     **Nhận xét:**
    #     """)
    
    # Visualization 2: Biểu đồ cột tổng Count cho mỗi Feature
    st.subheader('2. Biểu đồ cột biểu diễn tổng số lần xuất hiện của các nhóm từ khóa đánh giá sản phẩm')
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
        **Nhận xét:** Thông qua các phương thức trực quan hóa nêu trên, 
                nhóm rút ra được một số kết luận về sự quan tâm của các khách hàng như sau:
        - 3 nhóm từ khóa mà các khách hàng quan tâm nhất khi mua sắm trực tuyến một sản phẩm 
                điện tử là: chất lượng, dịch vụ, đặc điểm kỹ thuật.
        - Chất lượng: các khách hàng thường có các nhận xét chung chung về sản phẩm như 'tốt', 'chất lượng', 'ok', 'ổn',...
        - Dịch vụ: các khách hàng thường có nhiều sự quan tâm đến tốc độ giao hàng, 
                hình thức đóng gói, sự nhiệt tình trong phản hồi và tư vấn của người bán.
        - Đặc điểm kỹ thuật: đây là nhóm từ khóa có đa dạng các từ khóa con nhất, 
                mà trong đó sự quan tâm nổi trội nhất của người dùng thường là 'pin', 'màn hình', 'sạc', 'màu', 'chụp',... 
        """)
    
    # Visualization 3: Biểu đồ cột Keywords Count by Brand and Feature
    st.subheader('3. Biểu đồ cột biểu diễn tổng số lượng mỗi nhóm từ khóa cho từng nhãn hàng')
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
        **Nhận xét:** Thông qua biểu đồ này, có thể nhận thấy các nhãn hàng nhận được nhiều bình luận liên quan 
                đến các từ khóa đặc điểm sản phẩm, dịch vụ bao gồm Samsung, Apple, Oppo,... Bên cạnh đó, 
                cũng tương tự như đối với toàn bộ các từ khóa, nhóm từ khóa liên quan đến chất lượng, đặc điểm 
                kỹ thuật và dịch vụ là ba vấn đề mà người dùng quan tâm nhiều nhất trên đối tất cả các nhãn hiệu.
        """)
    
    # Visualization 4: Biểu đồ tròn tỷ lệ đặc tính cho các brand hàng đầu
    st.subheader('4. Biểu đồ tròn biểu diễn tỷ lệ giữa các nhóm từ khóa cho từng nhãn hàng')
    top_brands = df_new['brandName'].value_counts().nlargest(3).index.tolist()
    df_top = df_new[df_new['brandName'].isin(top_brands)]

    feature_columns = ['chất lượng_count', 'giá cả_count', 'thiết kế_count', 'hiệu năng_count', 'đặc điểm kỹ thuật_count', 'dịch vụ_count', 'tình trạng sản phẩm_count']
    df_feature_counts = df_top.groupby('brandName')[feature_columns].sum()
    df_feature_counts.columns = ['chất lượng', 'giá cả', 'thiết kế', 'hiệu năng', 'đặc điểm kỹ thuật', 'dịch vụ', 'tình trạng sản phẩm']

    df_feature_counts['tổng giá trị'] = df_feature_counts.sum(axis=1)
    df_feature_counts = df_feature_counts.sort_values(by='tổng giá trị', ascending=False)
    df_feature_counts = df_feature_counts.drop(columns=['tổng giá trị'])
   

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
    st.markdown("""
        **Nhận xét:**
        - Chất lượng luôn là đặc điểm được quan tâm nhiều nhất với tỷ lệ vượt trội trên 25% `so với toàn bộ các từ khóa.
        - Các khách hàng của nhãn hàng Samsung nhắc nhiều về các từ khóa dịch vụ hơn đặc điểm kỹ thuật, với sự chênh lệch xấp xỉ 4%.
        - Các khách hàng của Apple và Oppo nhắc đến nhiều về các đặc điểm kỹ thuật hơn, mà trong đó sự chênh lệch giữa hai đặc điểm này ở Apple là 1.5\% và khoảng 3\% đối với Oppo.
        - Trong khi đó, 4 đặc điểm còn lại có tổng số phần trăm từ khóa chỉ chiếm khoảng 30\%.
        """)

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
    plt.xlabel('Brand Name')
    plt.ylabel('Tỷ lệ nhắc đến')
    plt.legend(title='Đặc tính')
    plt.grid(axis='y')
    st.pyplot(fig)

    st.markdown("""
        **Nhận xét:**
        - Chất lượng: Apple và Samsung có tỷ lệ nhắc đến chất lượng cao nhất,
                 cho thấy người tiêu dùng rất chú trọng đến chất lượng khi đánh giá các sản phẩm của hai nhãn hiệu này.
        - Thiết kế: Oppo có tỷ lệ nhắc đến thiết kế cao hơn so với Apple và Samsung, 
                cho thấy người tiêu dùng rất quan tâm đến thiết kế của sản phẩm Oppo.
        - Đặc điểm kỹ thuật: Đặc điểm kỹ thuật được nhắc đến nhiều ở Oppo và Samsung, 
                cho thấy sự quan tâm lớn đến tính năng kỹ thuật của sản phẩm từ hai nhãn hiệu này.
        - Dịch vụ: Tỷ lệ nhắc đến dịch vụ khá cao ở Apple và Samsung, cho thấy chất lượng dịch vụ 
                là một yếu tố quan trọng trong các đánh giá của người tiêu dùng.
        """)
    
    openAi = OpenAIChatbot()
    appContext = AppContext.get_instance()
    appContext.titlePage = strings.get_string("review_hypothesis_title")[0]
    appContext.content = "Đây là trích xuất & phân tích những đặc điểm của sản phẩm thường được nhắc đến trong review"
    appContext.hyphothesisTitle = "Trích xuất & phân tích những đặc điểm của sản phẩm thường được nhắc đến trong review"

    # hpsContent sẽ là kết quả của phân tích
    hpsContent = (f"""Dưới đây là các nhóm từ khóa chính được phân tích, mỗi nhóm phản ánh một khía cạnh quan trọng của sản phẩm hoặc dịch vụ:
                  
            - Chất lượng: Các từ khóa này phản ánh cảm nhận của khách hàng về độ bền, độ tin cậy và chất lượng tổng thể của sản phẩm. Chúng cho biết mức độ hài lòng hoặc không hài lòng của khách hàng về chất lượng sản phẩm.
                  
            - Giá cả: Nhóm từ khóa này cho thấy sự quan tâm của khách hàng về mặt giá cả và chi phí. Nó giúp doanh nghiệp hiểu được mức độ hài lòng của khách hàng về giá trị mà họ nhận được so với số tiền bỏ ra.
                  
            - Thiết kế: Các từ khóa này phản ánh cảm nhận của khách hàng về thiết kế và hình thức của sản phẩm. Chúng giúp xác định mức độ ưa chuộng về mặt thẩm mỹ và kiểu dáng của sản phẩm.
                  
            - Hiệu năng: Nhóm từ khóa này liên quan đến hiệu suất và tốc độ hoạt động của sản phẩm. Nó cho thấy mức độ hài lòng của khách hàng về khả năng đáp ứng và vận hành của sản phẩm.
                  
            - Đặc điểm kỹ thuật: Các từ khóa này phản ánh những đặc điểm và tính năng kỹ thuật của sản phẩm. Chúng cho biết mức độ hài lòng của khách hàng về các tính năng cụ thể và hiệu quả của chúng.
                  
            - Dịch vụ: Nhóm từ khóa này liên quan đến dịch vụ khách hàng và hậu mãi. Nó giúp đánh giá chất lượng dịch vụ, sự hỗ trợ và mức độ hài lòng của khách hàng về dịch vụ mà họ nhận được.
                  
            - Tình trạng sản phẩm: Các từ khóa này phản ánh tình trạng thực tế của sản phẩm khi đến tay khách hàng. Nó giúp xác định các vấn đề liên quan đến tình trạng mới, cũ, hoặc hư hỏng của sản phẩm.""")
    appContext.hyphothesisContent = hpsContent
    appContext.prompt = "Dựa vào giả thuyết đặc điểm của sản phẩm thường được nhắc đến trong review trên hãy nhận xét cho tôi dạng markdown"
    response = openAi.generate_response(appContext) 

    st.markdown(response)

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

