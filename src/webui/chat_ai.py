import streamlit as st
import time
import numpy as np
from src.webui.session import Chat

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# page ui
st.set_page_config(page_title="聊天客服", page_icon="📞", layout="wide")

st.title("酒店在线客服")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("说些什么？"):
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        Chat.chainRag(question)
        full_response = "1111111144444444"
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
