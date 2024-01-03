from langchain.document_loaders.csv_loader import CSVLoader
from langchain.callbacks.base import BaseCallbackHandler
#from langchain.loaders import DirectoryLoader
import streamlit as st

from src.agent import create_agent
from src import MyCustomHandler
from src.sales_llm import LLM
from src.app import App


from google.oauth2 import service_account
from google.cloud import aiplatform
import json
import os

if __name__ == '__main__':
    with open("keys.json", "r") as api_keys_f: 
        api_keys = json.loads(api_keys_f.read())
        for key in api_keys.keys():
            os.environ[key] = api_keys[key]

    del api_keys_f, api_keys, key
    credentials = service_account.Credentials.from_service_account_file("C:/Users/Hugo/Documents/GenAI Front Basics Analysis/gkey.json")

    aiplatform.init(project="exploring-genai",
                credentials=credentials)

    app = App()
    llm = LLM()

    loader = CSVLoader(file_path='data/PlanosCelular-Planos.csv',
                       encoding="utf-8", 
                       csv_args={'delimiter': ','})
    data = loader.load()

    conversation_retrieval_chain = llm.init_conversation_retrieval_chain(data=data)
    conversation_chain = llm.init_conversation_chain()

    input = app.get_user_input()

    if input:
        # output = conversation_chain.predict(input=input)
        # print(f'conversation_chain output: {output}')

        output = conversation_retrieval_chain(inputs={"question": input, 
                                                      "chat_history": app.get_history()},
                                              return_only_outputs=True)

        app.set_generated_message_state(output['answer'])
        app.set_history(input, output['answer'])

    app.create_chat_component()
