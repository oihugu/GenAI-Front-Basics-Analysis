from os import environ
from typing import List
from langchain import HuggingFaceHub, PromptTemplate
from langchain.chains import ConversationalRetrievalChain, ConversationChain
from langchain.vectorstores import FAISS
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

from os import getenv, path

class LLM:
    def __init__(self) -> None:
        self.llm = ChatVertexAI(model_name="chat-bison-32k")
        self.conversation_memory = ConversationBufferMemory(return_messages=True,
                                                            memory_key='chat_history', 
                                                            input_key='question')

    def init_conversation_retrieval_chain(self, data: List[Document]) -> ConversationalRetrievalChain:
        embeddings = HuggingFaceHubEmbeddings(
            huggingfacehub_api_token=self.huggingface_api_token)
        vectorstore = FAISS.from_documents(data, embeddings)
        print(f'vector_store: {vectorstore}')

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "O que se segue é uma conversa amigável entre um humano e uma IA. A IA é falante e fornece muitos detalhes específicos de seu contexto. Se a IA não souber a resposta a uma pergunta, ela diz sinceramente que não sabe."),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        template = """Você é um vendedor que auxilia os clientes na escolha de um pacote para seus filhos. \
                    Seja gentil, convincente e faça com que eles comprem um pacote. Se você não sabe a resposta para uma pergunta \
                    simplesmente responda que você não sabe e que eles precisam falar com um humano para obter essa resposta. \
                    Forneça respostas em formato tabular se for solicitado a comparar pacotes.
        {chat_history}
        Human: {question}
        Salesbot:"""

        prompt = PromptTemplate(
            input_variables=['chat_history', 'question'],
            template=template,
            validate_template=True
        )

        chain = ConversationalRetrievalChain.from_llm(llm=self.llm,
                                                      retriever=vectorstore.as_retriever(),
                                                      verbose=True,
                                                      memory=self.conversation_memory,
                                                    #   condense_question_prompt=prompt
                                                      )

        print(f'conversation_retrieval_chain: {chain}')
        return chain

    def init_conversation_chain(self) -> ConversationChain:
        chain = ConversationChain(llm=self.llm,
                                  verbose=True,
                                #   memory=self.conversation_memory
                                  )
        print(f'conversation_chain: {chain}')
        return chain