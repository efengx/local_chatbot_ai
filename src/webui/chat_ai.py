import streamlit as st
from src.webui.session import Chat, session

session.setSession(count=20)

# page ui
st.set_page_config(page_title="聊天客服", page_icon="📞", layout="wide")

# 左侧边栏目
with st.sidebar:
    st.toggle(
        '调试模式', 
        key="is_cache",
        value=st.session_state['is_cache'],
    )
    
    st.text_area(
        "system message:",
        key="prompt_system",
        value=st.session_state['prompt_system'],
        height=200,
    )
    
    st.text_area(
        'system message context:',
        key="documents",
        value=st.session_state['documents'],
        height=200,
    )
    
    st.text_area(
        'human message:',
        key="prompt_human",
        value=st.session_state['prompt_human'],
        height=100,
    )
    
    st.text_area(
        'model params:',
        key="model_params",
        value=st.session_state['model_params'],
        height=100,
    )
        
st.write("酒店在线客服")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("question"):
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
