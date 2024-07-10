import streamlit as st
from String import StringManager

def hypothesisProductScreenPhuc(strings: StringManager):
    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("product_hypothesis_title")[0])
    # Todo: Tất cả trang này là về Giả Thuyết Của Phúc