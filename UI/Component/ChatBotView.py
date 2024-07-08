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

    with st.sidebar.form(key='my_form'):

        user_input = st.text_input(f"{strings.get_string('you')}:", key='user_input')
        submit_button = st.form_submit_button(label=f"{strings.get_string('send')}")

    if submit_button and user_input:
        appContext.prompt = user_input
        st.session_state['messages'].append({"You": user_input})

        response = ChatBot.OpenAIChatbot().generate_response(app_context=appContext)
        st.session_state['messages'].append({"Bot": response})

        # Clear the input field -> Nó còn bug, nào rãnh hả fix
        # st.session_state['user_input'] = ""

    for message in st.session_state['messages']:
        if 'You' in message:
            message_container.write(f"{strings.get_string('you')}: {message['You']}")
        else:
            message_container.write(f"{strings.get_string('bot')}: {message['Bot']}")