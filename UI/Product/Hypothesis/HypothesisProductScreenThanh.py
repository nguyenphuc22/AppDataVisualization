import streamlit as st
from String import StringManager
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from statsmodels.formula.api import ols
from DataManager.ProductManager import ProductManager

def hypothesisProductScreenThanh(strings: StringManager):
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

    st.pyplot(fig)

    # Kết luận và đề xuất dựa trên kết quả mô hình
    st.header("Kết luận & Khuyến nghị")

    pvalue = model.pvalues['price_encoded']
    coefficient = model.params['price_encoded']

    #Phần này nhờ đồng chị Thị Mai Nhi 
    if pvalue < 0.05:
        conclusion = f"(p-value = {pvalue:.4f}) nghĩa là mô hình dự đoán có giá trị thống kê và đáng tin cậy"
        if coefficient > 0:
            recommendation = "Khi giá tăng, số lượng bán có xu hướng tăng. Điều này có thể do các sản phẩm đắt tiền hơn thường có chất lượng cao hơn hoặc được ưa chuộng hơn."
        else:
            recommendation = "Khi giá tăng, số lượng bán có xu hướng giảm. Điều này phù hợp với quy luật cung cầu cơ bản."
    else:
        conclusion = f"Giá (price_encoded) không có ảnh hưởng đáng kể đến số lượng bán (p-value = {pvalue:.4f})"
        recommendation = "Cần xem xét các yếu tố khác có thể ảnh hưởng đến số lượng bán, như chất lượng sản phẩm, marketing, hoặc các yếu tố thị trường khác."

    st.markdown(f"**Kết luận:** {conclusion}")
    st.markdown(f"**Khuyến nghị:** {recommendation}")
