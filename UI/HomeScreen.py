import streamlit as st
from String import StringManager


def homeScreen(strings: StringManager):
    st.title(strings.get_string("home_title"))
    st.write(strings.get_string("welcome_message"))