# 全局session函数
import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 静态常量
template_prompt = """
鉴于此文本摘录：
-----
{context}
-----
请回答以下问题：
{question}
"""

documents = """
名迪城市酒店(尖沙咀) (Metacity Hotel (Tsim Sha Tsui)):
**酒店地址**：名迪城市酒店(尖沙咀) 位于中国香港香港香港尖沙咀这个地理位置便利，毗邻城市的主要景点和商业区域。
**房型：**名迪 - 標準雙人間,名迪 - 標準雙床房/雙人房,名迪 - 寬敞雙人間,名迪城市景觀 - 豪華家庭房,名迪城市景觀 - 豪華三人間,名迪城市豪华双人城景房,测试,钟点房测试宽敞而精致的名迪 - 標準雙人間配备现代化设施，为宾客提供一个温馨的栖息地，是商务旅行者和度假者的首选。
**酒店设施：**名迪城市酒店(尖沙咀) 通常提供婴儿床,洗衣服务,酒吧,可提供相连房,Wi-Fi上网(公共区域),停车场[附近],按摩,花园,家庭房,儿童游泳池,行李存放服务,电梯,出租车服务,儿童活动室,行李员,保姆(需预约),每日客房清洁服务,24小时前台,票务服务,可捞带宠物,按摩游泳池,酒店设停车场,洗衣机,餐厅,客房清洁服务(限定时周),旅游服务,地铁[附近],无障碍通道,干洗,水疗,游泳池,24小时送餐服务,健身中心,快速办理入住/退房,所有客房免费WiFi,无障碍设施,24小时办理入住,礼宾服务,健身中心(24 小时),送餐服务(有限时间),吸烟区,保险箱一系列豪华的设施，以确保客人在住宿期间享受到最大的舒适和便利。
如果您考虑入住我们名迪城市酒店，请拨打18600248705我们随时为您提供计划帮助。
"""

# 初始化
if 'ai_service' not in st.session_state:
    st.session_state['ai_service'] = os.getenv('HOST_PORT')

if 'template_prompt' not in st.session_state:
    st.session_state['template_prompt'] = template_prompt
    
if 'documents' not in st.session_state:
    st.session_state['documents'] = documents

# 函数封装
def data_get(key):
    return st.session_state[key]
    
# def data_set(key, value):
#     st.session_state[key] = value

# 获取data strage数据
class Data:
    
    def getStorageList(limit: int = 10, offset: int = 0):
        data_request = requests.get(
            "{0}data/storage/list".format(data_get("ai_service")), 
            params={"limit": limit, "offset": offset})
        print(data_request.url)
        print(data_request.text)

class Chat:
    
    def chainRag(question):
        chat_request = requests.post(
            "{0}chat/chain/rag".format(data_get("ai_service")),
            json={"question": question, "template_prompt": data_get('template_prompt'), "documents": data_get('documents')}
        )
        print(chat_request.url)
        print(chat_request.text)
