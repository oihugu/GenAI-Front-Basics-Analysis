from langchain.callbacks.base import BaseCallbackHandler
from utils.agent import create_agent
from utils import MyCustomHandler
import streamlit as st

if __name__ == '__main__':
    st.set_page_config(
        page_title="Chatbot",
        page_icon="💬",
    )

    st.write("""
    # Chatbot
    """)

    chat_container = st.container()
    agent = create_agent()

    user_prompt = st.chat_input(placeholder="Type a message...")
    if user_prompt:
        with chat_container.chat_message(name="User"):
            st.write(user_prompt)

        with chat_container.chat_message(name="ai"):
            handler = MyCustomHandler(BaseCallbackHandler, st)
            agent.run(user_prompt,
                      callbacks=[handler])

    print(agent.agent.llm_chain)