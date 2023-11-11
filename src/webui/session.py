# 全局session函数
import streamlit as st
import os
import json
from src.webui import model_chat_chain_rag
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class FxSession(object):

    count: Optional[int] = 0

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print("创新新的实例, 该实例的生命周期页面刷新时都不会丢失。只有代码更改时才会丢失")
            cls.instance = super(FxSession, cls).__new__(cls)
        return cls.instance

    def setSession(self, count: Optional[int] = None):
        print("初始化 fxSession count=", self.count)
        if count is not None:
            self.count = count
        
        if 'repository_name' not in st.session_state:
            st.session_state['repository_name'] = model_chat_chain_rag.repository_name
        
        if 'model_name' not in st.session_state:
            st.session_state['model_name'] = model_chat_chain_rag.model_name
        
        if 'is_cache' not in st.session_state:
            print("初始化 is_cache")
            st.session_state['is_cache'] = model_chat_chain_rag.is_cache

        if 'prompt_system' not in st.session_state:
            print("初始化 prompt_system")
            st.session_state['prompt_system'] = model_chat_chain_rag.prompt_system

        if 'documents' not in st.session_state:
            print("初始化 document")
            st.session_state['documents'] = model_chat_chain_rag.documents

        if "prompt_human" not in st.session_state:
            print("初始化 prompt_human")
            st.session_state['prompt_human'] = model_chat_chain_rag.prompt_human

        if "model_params" not in st.session_state:
            print("初始化 model_params")
            st.session_state['model_params'] = model_chat_chain_rag.model_params

        if "messages" not in st.session_state:
            print("初始化 messages")
            st.session_state.messages = []

        # 知识库 分页
        if "num_total" not in st.session_state:
            st.session_state['num_total'] = 10

        if "current_page" not in st.session_state:
            st.session_state['current_page'] = 1

        if "current_offset" not in st.session_state:
            st.session_state['current_offset'] = 0

        return self
    
    def document_update(self, option):
        st.session_state['documents'] = model_chat_chain_rag.map_document[option]

    def data_get(self, key):
        return st.session_state[key]


# 获取data strage数据

class Data:

    def getStorageList(offset: int, limit: int = 10):
        data_request = requests.get(
            "{0}data/storage/list".format(os.getenv('HOST_PORT')),
            params={"limit": limit, "offset": offset})
        return json.loads(data_request.text)


class Chat:

    def chainRag(question):
        data_json = {"load_model": "FxChatOpenAI",
                     "prompt_system": st.session_state['prompt_system'],
                     "documents": st.session_state['documents'],
                     "prompt_human": st.session_state['prompt_human'],
                     "question": question,
                     "is_cache": not bool(st.session_state['is_cache']),
                     "meta_data": st.session_state['model_params'],
                     "repository_name": model_chat_chain_rag.map_repository_name[st.session_state['repository_name']],
                     "model_name": st.session_state['model_name']}
        chat_request = requests.post(
            "{0}chat/chain/rag".format(os.getenv('HOST_PORT')),
            json=data_json
        )
        print("chat data_json:", data_json)
        return json.loads(chat_request.text)


# 开启单例模式
session = FxSession()
