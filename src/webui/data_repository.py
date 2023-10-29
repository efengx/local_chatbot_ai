import streamlit as st
import json
import pandas as pd
from src.webui.session import Data, session, Chat
from src.webui.components import Components
from io import StringIO

session.setSession()

st.set_page_config(
    page_title="知识库",
    page_icon="🗂️",
    layout="wide"
)


uploaded_file = st.file_uploader("选择知识库问题列表，并自动生成回复")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    dataframe = pd.read_csv(uploaded_file)

    def chainRag(index, row):
        result = Chat.chainRag(row.iloc[0])
        print(index, row.iloc[0], result)
    Components.ui_load_data(dataframe, chainRag)


label = "知识库：总页数{0}, 总条数{1}".format(
    round(st.session_state['num_total']/10), st.session_state['num_total'])
st.number_input(label, key="current_page",
                min_value=1,
                format="%d",
                step=1)                    # 分页

st.session_state['current_offset'] = (
    st.session_state['current_page'] - 1) * 10
if list_data := Data.getStorageList():
    st.session_state['num_total'] = list_data['count']
    items_data = list_data['items']
    if len(items_data) > 0:
        df = pd.DataFrame(items_data)
        def format(answer):
            return json.loads(answer)[0]['text']
        df["answer"] = df["answer"].apply(format)
        edited_df = st.data_editor(df, hide_index=True)
    else:
        st.write("第{0}页无数据".format(st.session_state['current_page']))