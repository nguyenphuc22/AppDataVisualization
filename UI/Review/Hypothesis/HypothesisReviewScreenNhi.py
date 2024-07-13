import streamlit as st
from String import StringManager

def hypothesisReviewScreenNhi(strings: StringManager):
    print("Hypothesis Review Screen Nhi Entry")

    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("review_hypothesis_title")[0])
    # Todo: Tất cả trang này là về Giả Thuyết Của Nhi