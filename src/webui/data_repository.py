import streamlit as st
import json
import pandas as pd
from src.webui.session import Data, session, Chat
from src.webui.components import Components
from src.webui import model_chat_chain_rag

session.setSession()

st.set_page_config(
    page_title="知识库",
    page_icon="🗂️",
    layout="wide"
)

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

    Components.ui_text_area(label="system message context:",
                            key="documents",
                            default_value=model_chat_chain_rag.map_document[st.session_state['repository_name']])

uploaded_file = st.file_uploader("选择知识库问题列表，并自动生成回复")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    dataframe = pd.read_csv(uploaded_file)
    Components.ui_load_data(dataframe=dataframe,
                            callback=lambda index, row: Chat.chainRag(row.iloc[0]))

label = "知识库：总页数{}, 总条数{}".format(
    round(st.session_state['num_total']/10 + 1), st.session_state['num_total'])
st.number_input(label, key="current_page",
                min_value=1,
                format="%d",
                step=1)                    # 分页

if list_data := Data.getStorageList(offset=(st.session_state['current_page'] - 1) * 10):
    st.session_state['num_total'] = list_data['count']
    items_data = list_data['items']
    if len(items_data) > 0:
        df = pd.DataFrame(items_data)

        # 格式化answer
        df["answer"] = df["answer"].apply(
            lambda answer: json.loads(answer)[0]['text'])

        # 格式化question
        df["question"] = df["question"].apply(lambda question: "{}:{}".format(
            [key for key, value in model_chat_chain_rag.map_repository_name.items() if question.split(":", 1)[0] in value][0], question.split(":", 1)[1]))
        edited_df = st.data_editor(df, hide_index=True)
    else:
        st.write("第{}页无数据".format(st.session_state['current_page']))
