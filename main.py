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

    user_prompt = st.chat_input(placeholder="Type a message...")
    if user_prompt:
        with chat_container.chat_message(name="User"):
            st.write(user_prompt)

        with chat_container.chat_message(name="ai"):
            st.write("I'm still learning, please try again later")