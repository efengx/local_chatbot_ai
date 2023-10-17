# Human operation
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['AI_SERVICE'] = 'http://127.0.0.1:8000'

ai_service = os.environ['AI_SERVICE']

st.set_page_config(layout="wide")

my_bar = st.progress(0, text="Operation in progress. Please wait...")

result = requests.get(url="{0}/progress".format(ai_service))
result = result.json()
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
