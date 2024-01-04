from typing import List

from langchain.chains import ConversationalRetrievalChain, ConversationChain, LLMChain
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
                                                            memory_key='history', 
                                                            input_key='input') # Uma lista de listas, quando vier do client para a API ele atualiza com o que vem do client, dependete por sessão

    def init_conversation_chain(self):

            template_files = ['prompts/IntroPrompt.txt', 'prompts/PlanosTextoLivre.txt']

            template = ''            
            with open(template_files[0], 'r', encoding='utf-8') as main_template:
                with open(template_files[0], 'r', encoding='utf-8') as sec_template:
                    template += main_template.read().replace('--planos_introducao--', sec_template.read())


            prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(
                    "Você é um vendedor de planos de celular. A IA é falante e fornece muitos detalhes específicos sobre planos de celular. Se a IA não souber a resposta a uma pergunta, ela diz sinceramente que não sabe."),
                # Podemos falar o que ele precisa fazer ao longo da conversa
                HumanMessagePromptTemplate.from_template(template)
            ])



            # Não passar um conversational chain, usar o exemplo do chat with tools

            # Para facilitar o embedding e os planos, podemos criar uma descrição em linguagem natural para cada plano
            # pode deixar mais tranquilo para o cliente


            chain = ConversationChain(memory=self.conversation_memory,
                                      llm=self.llm,
                                      prompt=prompt)

            return chain

