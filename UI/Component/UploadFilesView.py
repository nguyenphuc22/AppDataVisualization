import streamlit as st
import pandas as pd
from String import StringManager
from DataManager.ProductManager import ProductManager
from DataManager.ReviewManager import ReviewManager
from DataManager.DataManager import check_format

def uploadFilesView(strings: StringManager):
    # Initialize session state for upload results
    if 'upload_result' not in st.session_state:
        st.session_state['upload_result'] = {'valid': None, 'type': None, 'message': None}

    # Display the file uploader widget
    uploaded_file = st.sidebar.file_uploader(
        strings.get_string("file_uploader_title"),
        type=['csv', 'xlsx']
    )

    # Handle the uploaded file
    if uploaded_file is not None:
        # Process the uploaded file based on its type
        if uploaded_file.type == 'text/csv':
            new_data = pd.read_csv(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            new_data = pd.read_excel(uploaded_file)
        else:
            st.error(strings.get_string("unsupported_file_type"))
            return

        # Update the ProductManager or ReviewManager with the new data
        try:
            result = check_format(new_data)

            if result['valid']:
                st.session_state['file_type'] = result['type']
                st.session_state['upload_result'] = {
                    'valid': True,
                    'type': result['type'],
                    'message': f"File {result['type']} được upload thành công."
                }

                # Update the correct manager based on file type
                if result['type'] == 'product':
                    ProductManager.get_instance().update_data(new_data)
                elif result['type'] == 'review':
                    ReviewManager.get_instance().update_data(new_data)
            else:
                st.session_state['upload_result'] = {
                    'valid': False,
                    'type': None,
                    'message': strings.get_string("wrong_format")
                }

        except ValueError as e:
            st.session_state['upload_result'] = {
                'valid': False,
                'type': None,
                'message': f"Error: {e}"
            }

        # Display the results based on session state
        if st.session_state['upload_result']['message']:
            if st.session_state['upload_result']['valid']:
                st.success(st.session_state['upload_result']['message'])  # Success notification
            else:
                st.error(st.session_state['upload_result']['message'])  # Error notification

        # Reset upload_result after display
        st.session_state['upload_result'] = {'valid': None, 'type': None, 'message': None}
