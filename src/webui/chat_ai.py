import streamlit as st
import json
from src.webui.session import Chat, Session

Session()

# page ui
st.set_page_config(page_title="聊天客服", page_icon="📞", layout="wide")

st.write("酒店在线客服")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("说些什么？"):
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = Chat.chainRag(question)
        if response.get("result") is not None:
            full_response = response["result"]
        else:
            full_response = "服务器调用失败."
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
