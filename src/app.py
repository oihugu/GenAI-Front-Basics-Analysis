from typing import List
import streamlit as st
from streamlit_chat import message

class App():
    def __init__(self) -> None:
        self.chat_context = ""
        self.dashboard_title = 'Planos de Ceular'
        st.title(self.dashboard_title)

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Olá, Estou aqui para te ajudar a escolher seu plano de ceular"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Me ajude a escolher o melhor plano para o meu perfil."]

        if 'user_input' not in st.session_state:
            st.session_state['user_input'] = ''

        if 'history' not in st.session_state:
            st.session_state['history'] = []

        #container for the chat history
        self.response_container = st.container()
        
        #container for the user's text input
        self.container = st.container()

    def get_user_input(self):
        with self.container:
            with st.form(key='my_form', clear_on_submit=True):
                st.text_input('You: ', key='user_input')
                submit_button = st.form_submit_button(label='Send')

                if submit_button and st.session_state['user_input']:
                    st.session_state.past.append(st.session_state['user_input'])
                    return st.session_state['user_input']

                reset_button = st.form_submit_button(label='Reset')

                if reset_button:
                    self.reset_chat()
                    return None

    def set_generated_message_state(self, generated_text: str) -> None:
        st.session_state.generated.append(generated_text)

    def create_chat_component(self) -> None:
        if st.session_state['generated']:
            with self.response_container:
                for i in range(-1, len(st.session_state['generated'])-1, 1):
                    message(st.session_state['past'][i],
                            is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))
                    
                    
    def set_history(self, input: str, output: str) -> None:
        st.session_state.history.append((input, output))

    def get_history(self):
        return st.session_state['history']
    
    def reset_chat(self):
        #Clear cache
        st.runtime.legacy_caching.clear_cache()
        st.experimental_rerun()