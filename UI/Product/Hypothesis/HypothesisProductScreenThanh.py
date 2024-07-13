import streamlit as st
from String import StringManager

def hypothesisProductScreenThanh(strings: StringManager):
    print("Hypothesis Product Screen Thanh Entry")
    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("product_hypothesis_title")[1])
    # Todo: Tất cả trang này là về Giả Thuyết Của Thành