import os
import langchain
from typing import Any
from loguru import logger
# from langchain.callbacks import FileCallbackHandler
from src.chatbot.fx_llamacpp import LlamaCpp
from src.chatbot.fx_cache import fxCache
from langchain.cache import GPTCache
from src.chatbot.fx_open_llm import FxOpenAIChat
from langchain.embeddings import HuggingFaceEmbeddings
from src.chatbot.fx_chat_openai import FxChatOpenAI
from langchain.chains import LLMChain
from src.chatbot.fx_stuff_documents_chain import FxStuffDocumentsChain
from langchain.document_transformers import LongContextReorder
from langchain.vectorstores import Milvus
from langchain.llms import OpenAI
from src.chatbot.fx_chain_llm import FxLLMChain
from langchain.prompts import PromptTemplate
from src.chatbot.fx_callback import FxStdOutCallbackHandler
from src.chatbot.fx_llm import FxLLM
from dotenv import load_dotenv
from src.chatbot.fx_cache import FxCache
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()

class FxModel:
    map_llm = {
        "FxOpenAIChat": FxOpenAIChat,
        "FxChatOpenAI": FxChatOpenAI,
        "LlamaCpp": LlamaCpp,
    }
    
    @classmethod
    def getllm(cls, fx_model_type, **kwargs: Any,):
        cls.llm = cls.map_llm[fx_model_type](**kwargs)
        return cls.llm

class FxChat:
    
    @classmethod
    def getCache(cls, isCache: bool = True):
        if not isCache:
            fxCache.setCache(isCache)
        else:
            print("重启开启缓存")
            fxCache.getCache()
        return cls
    
    @classmethod
    def getModel(cls, fx_model_type, **kwargs: Any):
        print("初始化model, model_type=", fx_model_type)
        FxModel.getllm(fx_model_type, **kwargs)
        return cls
    
    @classmethod
    def chainRagLlm(cls, prompt_system: str, document: str, prompt_human: str, question: str, ):
        system_message_prompt = SystemMessagePromptTemplate.from_template(prompt_system)
        human_message_prompt = HumanMessagePromptTemplate.from_template(prompt_human)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        
        chain = FxLLMChain(llm=FxModel.llm, prompt=chat_prompt)
        
        # # 通过document重构提示模版
        # document_prompt = PromptTemplate(
        #     input_variables=["page_content"], 
        #     template="{page_content}"
        # )
        # # 该值与prompt中的template_prompt对应
        # document_variable_name = "context"
        # chain = FxStuffDocumentsChain(
        #     llm_chain=llm_chain,
        #     document_prompt=document_prompt,
        #     document_variable_name=document_variable_name,
        # )
        
        # 创建一个检索器，获取与question相关的文档
        # if not hasattr(cls, "embeddings"):
        #     cls.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

        # retriever = Milvus.from_texts(
        #     [document], 
        #     embedding=cls.embeddings,
        #     connection_args={"host": os.getenv('MILVUS_HOST')}).as_retriever(search_kwargs={"k": 1})
        # docs = retriever.get_relevant_documents(question)
        # print("docs=", docs)
        
        # 重新对文档进行排序，相关性较高的位于文档的开头和结尾，相关性较低的位于中间
        # reordering = LongContextReorder()
        # reordered_docs = reordering.transform_documents(docs)
        # print("reordered_docs=", reordered_docs)
        handler = FxStdOutCallbackHandler()
        result = chain.run(context=document, question=question, callbacks=[handler])
        return result
