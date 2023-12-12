from langchain.callbacks.base import BaseCallbackHandler
from src.agent import create_agent
from src import MyCustomHandler
import streamlit as st

# if __name__ == '__main__':
#     st.set_page_config(
#         page_title="Chatbot",
#         page_icon="💬",
#     )

#     st.write("""
#     # Chatbot
#     """)

#     if 'generated' not in st.session_state:
#         st.session_state['generated'] = ["Hello ! Ask me anything about anything 🤗"]

#     if 'past' not in st.session_state:
#         st.session_state['past'] = ["Hey ! 👋"]

#     if 'user_input' not in st.session_state:
#         st.session_state['user_input'] = '' 

#     if 'history' not in st.session_state:
#         st.session_state['history'] = []



#     chat_container = st.container()
#     agent = create_agent()

#     user_prompt = st.chat_input(placeholder="Type a message...")
#     if user_prompt:
#         with chat_container.chat_message(name="User"):
#             st.write(user_prompt)

#         with chat_container.chat_message(name="ai"):
#             handler = MyCustomHandler(BaseCallbackHandler, st)
#             agent.run(user_prompt,
#                       callbacks=[handler])

#     print(agent.agent.llm_chain)

from src.app import App
from src.agent import LLM
from langchain.document_loaders.csv_loader import CSVLoader

if __name__ == '__main__':
    app = App()
    llm = LLM()

    loader = CSVLoader(file_path='data\\PlanosCelular-Planos.csv',
                       encoding="utf-8", 
                       csv_args={'delimiter': ','})
    data = loader.load()
    print(f'data: {data}')

    conversation_retrieval_chain = llm.init_conversation_retrieval_chain(data)
    conversation_chain = llm.init_conversation_chain()

    input = app.get_user_input()

    if input:
        # output = conversation_chain.predict(input=input)
        # print(f'conversation_chain output: {output}')

        output = conversation_retrieval_chain(inputs={"question": input, 
                                                      "chat_history": app.get_history()},
                                              return_only_outputs=True)

        print(f'conversation_retrieval_chain output: {output}')
        app.set_generated_message_state(output['answer'])
        app.set_history(input, output['answer'])

    app.create_chat_component()