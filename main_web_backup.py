# Human operation
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ai_service = os.getenv('HOST_PORT')

# 页面全局样式
st.set_page_config(layout="wide")

# web api fun
def chat_rag():
    result_chat_rag = requests.post(url="{0}/chat/chain/rag".format(ai_service), )
    result = result_chat_rag.json()
    print(result)
    print(result['progress'])
    print(result['maxProgress'])

# while my_app.progress < 5:
#     my_bar.progress(my_app.progress, text=f"Progress: {my_app.progress}%")

# 侧边栏
with st.sidebar:
    pass

with st.form("form_query"):
    query = st.text_input("query")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("query=", query)
