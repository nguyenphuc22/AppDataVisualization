import streamlit as st

import ChatBot
from AppContext import AppContext

import streamlit as st

import ChatBot
from AppContext import AppContext
from String import StringManager


def chatbotView():
    appContext = AppContext.get_instance()
    strings = StringManager.get_instance()

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    st.sidebar.title(strings.get_string('chatbot_title'))

    message_container = st.sidebar.container()

    # Use a callback function to handle new messages
    def handle_new_message():
        user_input = st.session_state.user_input
        if user_input:  # Check if there's any input
            appContext.prompt = user_input
            response = ChatBot.OpenAIChatbot().generate_response(app_context=appContext)
            # Append both user and bot messages
            st.session_state['messages'].append({"You": user_input, "Bot": response})
            # Clear the input field by resetting the session state variable
            st.session_state.user_input = ""

    # Text input with on_change callback to handle new messages
    user_input = st.sidebar.text_input(f"{strings.get_string('you')}:", key='user_input', on_change=handle_new_message)

    # Display messages
    for message in st.session_state['messages']:
        if 'You' in message:
            message_container.markdown(f"<div style='color: cyan; text-align: right;'>{strings.get_string('you')}: {message['You']}</div>", unsafe_allow_html=True)
        if 'Bot' in message:
            message_container.markdown(f"<div style='text-align: left;'>{strings.get_string('bot')}: {message['Bot']}</div>", unsafe_allow_html=True)