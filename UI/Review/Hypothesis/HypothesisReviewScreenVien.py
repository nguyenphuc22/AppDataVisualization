import streamlit as st
from String import StringManager

def hypothesisReviewScreenVien(strings: StringManager):
    print("Hypothesis Review Screen Vien Entry")

    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("review_hypothesis_title")[1])
    # Todo: Tất cả trang này là về Giả Thuyết Của Viên