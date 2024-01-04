from langchain.document_loaders.json_loader import JSONLoader
from langchain.callbacks.base import BaseCallbackHandler
#from langchain.loaders import DirectoryLoader
import streamlit as st

from src import MyCustomHandler
from src.sales import LLM
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
    credentials = service_account.Credentials.from_service_account_file("gkey.json")

    aiplatform.init(project="exploring-genai",
                credentials=credentials)

    llm = LLM()
    app = App(llm)

    conversation_chain = llm.init_conversation_chain()

    input = app.get_user_input()

    if input:
        # output = conversation_chain.predict(input=input)
        # print(f'conversation_chain output: {output}')

        output = conversation_chain(inputs={"input": input, 
                                            "chat_history": app.get_history()},
                                            return_only_outputs=True)

        print(f'conversation_chain output: {output}')
        app.set_generated_message_state(output['output'])
        app.set_history(input, output['output'])

    app.create_chat_component()
