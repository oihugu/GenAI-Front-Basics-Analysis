from typing import List
import streamlit as st
from streamlit_chat import message

class App():
    def __init__(self, llm) -> None:
        self.chat_context = ""
        self.dashboard_title = 'Planos de Ceular'
        self.llm = llm
        st.title(self.dashboard_title)

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Olá, eu uma IA construida para te ajudar a escolher seu próximo plano de celular, me conte sobre suas preferências que te ajudarei."]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Olá"]

        if 'user_input' not in st.session_state:
            st.session_state['user_input'] = ''

        if 'chat_history' not in st.session_state:
            st.session_state['history'] = []

        #container for the chat history
        self.response_container = st.container()
        
        #container for the user's text input
        self.container = st.container()

    def get_user_input(self):
        with self.container:
            with st.divider():
                st.button(label='Log', on_click=self.create_log, use_container_width=True)
            
            with st.form(key='my_form', clear_on_submit=True):
                st.text_input('You: ', key='user_input')
                submit_button = st.form_submit_button(label='Send', type='primary', use_container_width=True)

                if submit_button and st.session_state['user_input']:
                    st.session_state.past.append(st.session_state['user_input'])
                    return st.session_state['user_input']
                
                st.form_submit_button(label='Reset', on_click=self.reset_chat, use_container_width=True)


        
    def set_generated_message_state(self, generated_text: str) -> None:
        st.session_state.generated.append(generated_text)

    def create_chat_component(self) -> None:
        if st.session_state['generated']:
            with self.response_container:
                for i in range(len(st.session_state['generated'])):
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
    
    def get_history(self):
        return st.session_state['history']
    
    def create_log(self):
        import datetime
        with open(f'logs/log-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w', encoding='utf-8') as f:
            for i in range(len(st.session_state['generated'])):
                f.write(f'User: {st.session_state["past"][i]}\n')
                f.write(f'LLM: {st.session_state["generated"][i]}\n')
                f.write('\n')
            f.write(f'Info: {self.llm.extract_information()}')