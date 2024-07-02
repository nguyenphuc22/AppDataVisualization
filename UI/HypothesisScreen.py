import streamlit as st
from String import StringManager

def hypothesisScreen(strings: StringManager):
    st.title(strings.get_string("hypothesis_title"))
    st.write(strings.get_string("hypothesis_message"))