import streamlit as st
import pandas as pd
from String import StringManager
from DataManager.ProductManager import ProductManager  # Import ProductManager
from DataManager.ReviewManager import ReviewManager  # Import ReviewManager

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
            # Change the file uploader key to force re-render
            st.session_state['file_uploader_key'] = f"file_uploader_{hash(str(st.session_state['file_uploader_key']))}"

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
                result = None
                if 'reviewContent' in new_data.columns:
                    review_manager = ReviewManager.get_instance()
                    result = review_manager.check_format(new_data)
                else:
                    product_manager = ProductManager.get_instance()
                    result = product_manager.check_format(new_data)

                if result['valid']:
                    st.session_state['file_type'] = result['type']
                    if result['type'] == 'review':
                        review_manager.update_data(new_data)
                    elif result['type'] == 'product':
                        product_manager.update_data(new_data)
                else:
                    st.error(strings.get_string("wrong_format"))

            except ValueError as e:
                st.error(f"Error: {e}")

            # Display the uploaded data
            # st.rerun()