import streamlit as st
import pandas as pd
from String import StringManager

def uploadFilesView(strings: StringManager):
    # Initialize session state for file uploader key
    if 'file_uploader_key' not in st.session_state:
        st.session_state['file_uploader_key'] = 'file_uploader_0'

    # Display the file uploader widget with dynamic key
    uploaded_file = st.sidebar.file_uploader(
        strings.get_string("file_uploader_title"),
        type=['csv', 'xlsx'],
        key=st.session_state['file_uploader_key']
    )

    # Handle the uploaded file
    if uploaded_file is not None:
        # Process the file here...
        if st.sidebar.button(strings.get_string("update_button")):
            # Change the file uploader key
            st.session_state['file_uploader_key'] = f"file_uploader_{hash(str(st.session_state['file_uploader_key']))}"
            # TODO: Cập nhật file mới vào data nhé Bình
            st.experimental_rerun()

