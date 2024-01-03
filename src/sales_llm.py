import os
from typing import List
from langchain import HuggingFaceHub, PromptTemplate
from langchain.chains import ConversationalRetrievalChain, ConversationChain, LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import VertexAIEmbeddings
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from langchain.chat_models import ChatVertexAI
from langchain.docstore.document import Document
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.prompts import format_document


from google.oauth2 import service_account
from google.cloud import aiplatform

credentials = service_account.Credentials.from_service_account_file("C:/Users/Hugo/Documents/GenAI Front Basics Analysis/gkey.json")

aiplatform.init(project="exploring-genai",
                credentials=credentials)

doc_prompt = PromptTemplate.from_template("{page_content}")

chain = (
    {
        "content": lambda docs: "\n\n".join(
            format_document(doc, doc_prompt) for doc in docs
        )
    }
    | PromptTemplate.from_template("Summarize the following content:\n\n{content}")
    | ChatVertexAI()
    | StrOutputParser()
)

from os import getenv, path

class LLM:
    def __init__(self) -> None:
        self.llm = ChatVertexAI(model_name="chat-bison-32k")
        self.conversation_memory = ConversationBufferMemory(return_messages=True,
                                                            memory_key='history', 
                                                            input_key='question') # Uma lista de listas, quando vier do client para a API ele atualiza com o que vem do client, dependete por sessão

    def init_conversation_retrieval_chain(self, data: List[Document]) -> ConversationalRetrievalChain:
        embeddings = VertexAIEmbeddings(
            model_name="textembedding-gecko-multilingual@latest"
        )
        vectorstore = FAISS.from_documents(data, embeddings) # Onde podemos fazer o pickle e salvar no GCS

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "O que se segue é uma conversa amigável entre um humano e uma IA. A IA é falante e fornece muitos detalhes específicos de seu contexto. Se a IA não souber a resposta a uma pergunta, ela diz sinceramente que não sabe."),
            # Podemos falar o que ele precisa fazer ao longo da conversa
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        # template = """Você é um vendedor que auxilia os clientes na escolha de um pacote de celular. \
        #             Seja gentil, convincente e faça com que eles comprem um pacote. Se você não sabe a resposta para uma pergunta \
        #             simplesmente responda que você não sabe e que eles precisam falar com um humano para obter essa resposta. \
        #             Forneça respostas de modo amigavel e passo a passo. Destaque os benefícios que já foram citados pelo cliente \

        #             Para recomendar um plano faça perguntas para o cliente até obter no minimo 5 das seguintes informações sobre suas preferências: \
        #             Tipo de plano: Pós-Pago ou Pré-Pago\
        #             Categoria de plano: individual ou de família\
        #             Valor de plano: O valor máximo que o cliente está disposto a pagar\
        #             Volume de consumo de dados: Alto, Médio ou Baixo \
        #             Portabilidade: Vai fazer a portabilidade de outra operadora? Sim ou Não\
        #             Frequência de viagens internacionais: Alta, Média ou Baixa\
        #             Preferência de conteúdo: Filmes, Futebol, TV, Novela ou Música\

        # {chat_history}
        # Human: {question}
        # Salesbot:"""
        template = """Você é um vendedor que auxilia os clientes na escolha de um pacote de celular. \
                    Seja gentil, convincente e faça com que eles comprem um pacote. Se você não sabe a resposta para uma pergunta \
                    simplesmente responda que você não sabe e que eles precisam falar com um humano para obter essa resposta. \
                    Em cada resposta mostre um json com as informações relevantes que você usou para chegar naquela resposta. \

                    Para recomendar um plano faça perguntas para o cliente até obter no minimo 5 das seguintes informações sobre suas preferências: \
                    Tipo de plano: Pós-Pago ou Pré-Pago\
                    Categoria de plano: individual ou de família\
                    Valor de plano: O valor máximo que o cliente está disposto a pagar\
                    Volume de consumo de dados: Alto, Médio ou Baixo \
                    Portabilidade: Vai fazer a portabilidade de outra operadora? Sim ou Não\
                    Frequência de viagens internacionais: Alta, Média ou Baixa\
                    Preferência de conteúdo: Filmes, Futebol, TV, Novela ou Música\

        {chat_history}
        Human: {question}
        Salesbot:"""

        # Não passar um conversational chain, usar o exemplo do chat with tools
        
        # Para facilitar o embedding e os planos, podemos criar uma descrição em linguagem natural para cada plano
        # pode deixar mais tranquilo para o cliente


        question_generator_chain = LLMChain(llm=self.llm, prompt=prompt)
        
        
        
        chain = ConversationalRetrievalChain(retriever=vectorstore.as_retriever(),
                                                      verbose=True,
                                                      memory=self.conversation_memory,
                                                      question_generator=question_generator_chain,
                                                      combine_docs_chain=chain,
                                                      )

        return chain

    def init_conversation_chain(self) -> ConversationChain:
        chain = ConversationChain(llm=self.llm,
                                  verbose=True,
                                  memory=self.conversation_memory)
        print(f'conversation_chain: {chain}')
        return chain