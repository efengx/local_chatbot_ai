import streamlit as st
from src.webui.session import Chat, session
from src.webui.components import Components
from src.webui import model_chat_chain_rag

session.setSession(count=20)

# page ui
st.set_page_config(page_title="聊天客服", page_icon="📞", layout="wide")

# 左侧边栏目
with st.sidebar:
    Components.ui_selectbox(label="请选择所属酒店",
                            key="repository_name",
                            options=["名迪旺角(metacity mk)",
                                     "名迪港岛酒店(铜锣湾) (Metaplace Hotel (Causeway Bay))",
                                     "名迪城市酒店(尖沙咀) (Metacity Hotel (Tsim Sha Tsui))",
                                     "default"],
                            default_value=model_chat_chain_rag.repository_name,
                            on_change_fun=lambda key: session.document_update(st.session_state[key]))

    Components.ui_selectbox(label="请选择模型",
                            key="model_name",
                            options=["gpt-4-1106-preview",
                                     "gpt-4"],
                            default_value=model_chat_chain_rag.model_name)

    Components.ui_toggle(label="调试模式",
                         key='is_cache',
                         default_value=model_chat_chain_rag.is_cache)
    
    Components.ui_text_area(label="system message:",
                            key="prompt_system",
                            default_value=model_chat_chain_rag.prompt_system)
    print("===", st.session_state['prompt_system'])

    Components.ui_text_area(label="system message context:",
                            key="documents",
                            default_value=model_chat_chain_rag.map_document[st.session_state['repository_name']])

    Components.ui_text_area(label="human message:",
                            key="prompt_human",
                            default_value=model_chat_chain_rag.prompt_human,
                            height=100)

    Components.ui_text_area(label="model params:",
                            key="model_params",
                            default_value=model_chat_chain_rag.model_params,
                            height=100)

st.write("在线客服")

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
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
