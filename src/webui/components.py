import streamlit as st
import time
from src.webui.session import session

session.setSession()

class Components:
    
    @classmethod
    def ui_load_data(cls, dataframe, callback):
        progress_text = "{0}加载中,请稍后...".format("")
        load_repository = st.progress(0.0, text=progress_text)
        for index, row in dataframe.iterrows():
            progress_text = "{0} {1} 加载中,请稍后...".format(f"{index}/{dataframe.shape[0] - 1}", row.iloc[0])
            load_repository.progress(1/(dataframe.shape[0])*index, text=progress_text)
            time.sleep(4)
            callback(index, row)
        time.sleep(1)
        load_repository.empty()
        
    @classmethod
    def ui_selectbox(cls, label, key, options, default_value, on_change_fun = None):
        if key not in st.session_state:
            st.session_state[key] = default_value
        
        st.selectbox(
            label,
            options,
            key=key,
            placeholder="Select contact method...",
        )
        if on_change_fun is not None:
            on_change_fun(key)
    
    
    @classmethod
    def ui_text_area(cls, label, key, default_value, height: int = 200):
        if key not in st.session_state:
            st.session_state[key] = default_value
        
        st.text_area(
            label,
            key=key,
            height=height,
        )
    
    @classmethod
    def ui_toggle(cls, label, key, default_value):
        if key not in st.session_state:
            st.session_state[key] = default_value
            
        st.toggle(
            label,
            key=key,
        )