import streamlit as st
from String import StringManager
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from statsmodels.formula.api import ols
from DataManager.ProductManager import ProductManager
from AppContext import AppContext
from ChatBot import OpenAIChatbot
from FixedContent import FixedContent

def hypothesisProductScreenThanh(strings: StringManager):
    print("Hypothesis Product Screen Thanh Entry")
    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("product_hypothesis_title")[1])
    # Todo: Tất cả trang này là về Giả Thuyết Của Thành
    productManager = ProductManager.get_instance() 

    df_cleaned = productManager.data

    # Mã hóa biến phân loại
    le = LabelEncoder()

    df_cleaned['brand_encoded'] = le.fit_transform(df_cleaned['brandName'])
    df_cleaned['price_encoded'] = le.fit_transform(df_cleaned['priceShow'])

    # Tạo mô hình OLS dựa trên biến được chọn
    formula = 'itemSoldCntShow ~ price_encoded'
    model = ols(formula, data=df_cleaned).fit()

    # Hiển thị tóm tắt kết quả mô hình
    st.header("Kết quả hồi quy OLS")

    st.write(model.summary())

    # Hiển thị biểu đồ phân tán dựa trên biến được chọn
    st.subheader("Biểu đồ phân tán")

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.scatterplot(x="priceShow", y='itemSoldCntShow', data=df_cleaned, ax=ax)
    ax.set_title("Price vs Số lượng bán")
    ax.set_xlabel("Price")
    ax.set_ylabel("Số lượng bán")

    plt.tight_layout()

    plt.savefig('ChatBotUtils/image/products_priceImpact_clusterchart.png')
    st.pyplot(fig)

    # Kết luận và đề xuất dựa trên kết quả mô hình
    st.header("Kết luận & Khuyến nghị")
    openAi = OpenAIChatbot()

     # Update AppContext
    appContext = AppContext.get_instance()
    appContext.titlePage = strings.get_string("product_hypothesis_title")[1]
    appContext.content = "Đây là giả thuyết ols xem các biến giá bán có ảnh hưởng đến số lượng bán hay không."
    appContext.hyphothesisTitle = "Giả thuyết sử dụng OLS trên tập dữ liệu số lượng bản Lazada"
    hpsContent = (f"Kết quả mô hình OLS: \n {model.summary().as_text()} \n")

    appContext.hyphothesisContent = hpsContent
    appContext.prompt = "Dựa vào kết quả OLS bên trên, hãy nhận xét và đưa ra kết luận cho tôi, ở định dạng markdown"

    fixedContent = FixedContent.get_instance()
    fixedContent.products_priceImpact_olsResult = hpsContent

    response = openAi.generate_response(appContext)
    st.markdown(f"<div style='color: cyan; text-align: right;'>{strings.get_string('you')}: {appContext.prompt}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: left;'>{strings.get_string('bot')}:\n\n {response}</div>", unsafe_allow_html=True)
