import streamlit as st
from String import StringManager

def hypothesisProductScreenBinh(strings: StringManager):
    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("product_hypothesis_title")[2])
    # Todo: Tất cả trang này là về Giả Thuyết Của Bình