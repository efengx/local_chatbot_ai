import streamlit as st
import json
import pandas as pd
from src.webui.session import Data, Session
from streamlit_elements import elements, mui, html
from streamlit_elements import dashboard

Session()

st.set_page_config(
    page_title="知识库", 
    page_icon="🗂️",
    layout="wide"
)

st.text_area(
    "提示结构：",
   st.session_state['template_prompt'],
   height=200
)

st.text_area(
    '附加文档：',
   st.session_state['documents'],
   height=200
)

st.write("知识库：")
if list_data := Data.getStorageList():
    df = pd.DataFrame(list_data['items'])
    
    # print(df["answer"])
    # print(df["answer"][0])
    # print(json.loads(df["answer"][0])[0]['text'])
    
    def format(answer):
        return json.loads(answer)[0]['text']
    df["answer"] = df["answer"].apply(format)
    
    edited_df = st.data_editor(df)
    # favorite_command = edited_df.loc[edited_df["answer"].idxmax()]["question"]
