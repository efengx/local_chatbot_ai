# 全局session函数
import streamlit as st
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# 静态常量
prompt_system = """
您好GPT，请扮演一个香港小型酒店客服并根据以下context去回答问题，如果context未涵盖问题，请根据你的知识库来回答问题,甚至是猜测，尽你最大可能去回答问题而不是回避问题。一定要注意这些事项：
不要暴露出自己是ai；
不要表示出你是根据context来回答问题的，如果context里面没有涉及到问题，就直接回答问题，不要回答信息不够或者没有提及；
不要让回答让客人打电话去询问，除非客人是直接询问电话号码；
可以基于常识的理解去回答；

context为：
{context}
"""

documents = """
名迪城市酒店(尖沙咀) (Metacity Hotel (Tsim Sha Tsui)):
**酒店地址**：名迪城市酒店(尖沙咀) 位于中国香港香港香港尖沙咀这个地理位置便利，毗邻城市的主要景点和商业区域。
**房型：**名迪 - 標準雙人間,名迪 - 標準雙床房/雙人房,名迪 - 寬敞雙人間,名迪城市景觀 - 豪華家庭房,名迪城市景觀 - 豪華三人間,名迪城市豪华双人城景房,测试,钟点房测试宽敞而精致的名迪 - 標準雙人間配备现代化设施，为宾客提供一个温馨的栖息地，是商务旅行者和度假者的首选。
**酒店设施：**名迪城市酒店(尖沙咀) 通常提供婴儿床,洗衣服务,酒吧,可提供相连房,Wi-Fi上网(公共区域),停车场[附近],按摩,花园,家庭房,儿童游泳池,行李存放服务,电梯,出租车服务,儿童活动室,行李员,保姆(需预约),每日客房清洁服务,24小时前台,票务服务,可捞带宠物,按摩游泳池,酒店设停车场,洗衣机,餐厅,客房清洁服务(限定时周),旅游服务,地铁[附近],无障碍通道,干洗,水疗,游泳池,24小时送餐服务,健身中心,快速办理入住/退房,所有客房免费WiFi,无障碍设施,24小时办理入住,礼宾服务,健身中心(24 小时),送餐服务(有限时间),吸烟区,保险箱一系列豪华的设施，以确保客人在住宿期间享受到最大的舒适和便利。
如果您考虑入住我们名迪城市酒店，请拨打18600248705我们随时为您提供计划帮助。
"""

prompt_human = """{question}"""

model_params = json.dumps({"temperature": 0.8, "n": 1, "organization": ""})

# 初始化


class FxSession(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FxSession, cls).__new__(cls)
        return cls.instance

    def setSession(self):
        print("初始化fxSession")
        if 'is_cache' not in st.session_state:
            st.session_state['is_cache'] = False

        if 'prompt_system' not in st.session_state:
            st.session_state['prompt_system'] = prompt_system

        if 'documents' not in st.session_state:
            print("init document")
            st.session_state['documents'] = documents

        if "prompt_human" not in st.session_state:
            st.session_state['prompt_human'] = prompt_human
            
        if "model_params" not in st.session_state:
            st.session_state['model_params'] = model_params

        if "messages" not in st.session_state:
            st.session_state.messages = []

        return self

    def data_get(key):
        return st.session_state[key]

# 获取data strage数据


class Data:

    def getStorageList(limit: int = 10, offset: int = 0):
        data_request = requests.get(
            "{0}data/storage/list".format(os.getenv('HOST_PORT')),
            params={"limit": limit, "offset": offset})
        print(data_request.url)
        # print(data_request.text)
        return json.loads(data_request.text)


class Chat:

    def chainRag(question):
        data_json = {"load_model": "FxChatOpenAI",
                     "prompt_system": st.session_state['prompt_system'],
                     "documents": st.session_state['documents'],
                     "prompt_human": st.session_state['prompt_human'],
                     "question": question,
                     "is_cache": not bool(st.session_state['is_cache']),
                     "meta_data": st.session_state['model_params']}
        chat_request = requests.post(
            "{0}chat/chain/rag".format(os.getenv('HOST_PORT')),
            json=data_json
        )
        return json.loads(chat_request.text)


# 开启单例模式
session = FxSession()
