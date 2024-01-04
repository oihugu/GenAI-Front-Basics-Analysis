from typing import List

from langchain.agents import AgentType, Tool, initialize_agent
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import VertexAIEmbeddings
from langchain.docstore.document import Document
from langchain.chat_models import ChatVertexAI


from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from google.oauth2 import service_account
from google.cloud import aiplatform



class LLM:
    def __init__(self) -> None:
        self.llm = ChatVertexAI(model_name="chat-bison-32k")
        self.conversation_memory = ConversationBufferMemory(return_messages=True,
                                                            memory_key='chat_history', 
                                                            input_key='input') # Uma lista de listas, quando vier do client para a API ele atualiza com o que vem do client, dependete por sessão

    def init_conversation_chain(self):

            template_files = ['prompts/IntroPrompt.txt', 'prompts/PlanosTextoLivre.txt']

            template = ''            
            with open(template_files[0], 'r', encoding='utf-8') as main_template:
                with open(template_files[0], 'r', encoding='utf-8') as sec_template:
                    template += main_template.read().replace('--planos_introducao--', sec_template.read())



            # Não passar um conversational chain, usar o exemplo do chat with tools

            # Para facilitar o embedding e os planos, podemos criar uma descrição em linguagem natural para cada plano
            # pode deixar mais tranquilo para o cliente
            tools = []

            return initialize_agent(tools = [],
                                    llm=self.llm,
                                    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                    agent_kwargs={"prefix": template,
                                                  "memory": self.conversation_memory,
                                                  "verbose": True}
                                    )


    # LLM Extratora - A parte da sales LLM mas ainda na mesma classe pelo histórico de conversa
    ## Com base no histórico de conversa, extrai as informações necessárias para o vendedor em um JSON
    def extract_information(self) -> dict:
    
        prompt=ChatPromptTemplate.from_messages([
                                HumanMessagePromptTemplate.from_template_file('prompts\ExtraçãoDeInformação.txt', input_variables=['chat_history']),
                                ])
        
        llm_lcel = prompt | ChatVertexAI(model_name="chat-bison-32k") | StrOutputParser()

        return llm_lcel.invoke({"chat_history": self.conversation_memory})