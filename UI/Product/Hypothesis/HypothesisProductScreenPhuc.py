import streamlit as st
from AppContext import AppContext
from ChatBot import OpenAIChatbot
from DataManager.ProductManager import ProductManager
from String import StringManager
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
import seaborn as sns


def hypothesisProductScreenPhuc(strings: StringManager):
    print("Hypothesis Product Screen Phuc Entry")

    st.title(strings.get_string("product_hypothesis_title")[0])

    productManager = ProductManager.get_instance()

    df_cleaned = productManager.data

    # Mã hóa biến phân loại
    le = LabelEncoder()
    df_cleaned['brand_encoded'] = le.fit_transform(df_cleaned['brandName'])
    df_cleaned['location_encoded'] = le.fit_transform(df_cleaned['location'])

    # Tính toán Discount
    df_cleaned['discount'] = (df_cleaned['originalPrice'] - df_cleaned['priceShow']) / df_cleaned['originalPrice']

    # Tạo sidebar cho người dùng chọn biến
    st.sidebar.header("Tùy chọn phân tích")
    selected_vars = st.sidebar.multiselect("Chọn biến giải thích",
                                           ['brand_encoded', 'location_encoded', 'discount', 'ratingScore'],
                                           default=['brand_encoded', 'location_encoded', 'discount', 'ratingScore'])

    # Tạo mô hình OLS dựa trên biến được chọn
    formula = 'itemSoldCntShow ~ ' + ' + '.join(selected_vars)
    model = ols(formula, data=df_cleaned).fit()

    # Hiển thị tóm tắt kết quả mô hình
    st.header("Kết quả hồi quy OLS")
    st.write(model.summary())

    # Hiển thị biểu đồ phân tán dựa trên biến được chọn
    st.subheader("Biểu đồ phân tán")
    n_vars = len(selected_vars)
    n_rows = (n_vars + 1) // 2
    n_cols = 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 6*n_rows))

    for i, var in enumerate(selected_vars):
        row = i // 2
        col = i % 2
        sns.scatterplot(x=var, y='itemSoldCntShow', data=df_cleaned, ax=axes[row, col])
        axes[row, col].set_title(f"{var} vs Số lượng bán")

    plt.tight_layout()
    st.pyplot(fig)

    # Kết luận và đề xuất dựa trên kết quả mô hình
    st.header("Kết luận & Khuyến nghị")
    openAi = OpenAIChatbot()

    # Update AppContext
    appContext = AppContext.get_instance()
    appContext.titlePage = strings.get_string("product_hypothesis_title")[0]
    appContext.content = "Giả thuyết sử dụng OLS trên tập dữ liệu số lượng bản Lazada"
    appContext.hyphothesisTitle = "Giả thuyết sử dụng OLS trên tập dữ liệu số lượng bản Lazada, Đây là giả thuyết ols xem các biến nào có ảnh hưởng đến số lượng bán hay không."
    # hpsContent sẽ là kết quả của mô hình OLS và kết luận từ mô hình
    hpsContent = (f"Kết quả mô hình OLS: \n {model.summary().as_text()} \n")
 
    appContext.hyphothesisContent = hpsContent
    appContext.prompt = "Dựa vào kết quả OLS bên trên, hãy nhận xét OLS cho tôi về giả thuyết biến có ảnh hưởng đến số lượng bán hay không ? trả về dạng markdown"
    response = openAi.generate_response(appContext)

    st.markdown(response)


