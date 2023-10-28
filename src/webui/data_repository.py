import streamlit as st
import json
import pandas as pd
from src.webui.session import Data, session
from streamlit_elements import elements, mui, html
from streamlit_elements import dashboard

session.setSession()

st.set_page_config(
    page_title="知识库",
    page_icon="🗂️",
    layout="wide"
)

st.write("知识库")

if list_data := Data.getStorageList():
    print(list_data)
    df = pd.DataFrame(list_data['items'])

    def format(answer):
        return json.loads(answer)[0]['text']
    df["answer"] = df["answer"].apply(format)

    edited_df = st.data_editor(df)