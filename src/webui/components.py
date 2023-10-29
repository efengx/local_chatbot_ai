import streamlit as st
import time

class Components:
    
    @classmethod
    def ui_load_data(cls, dataframe, callback):
        progress_text = "{0}加载中,请稍后...".format("")
        load_repository = st.progress(0.0, text=progress_text)
        for index, row in dataframe.iterrows():
            progress_text = "{0} {1} 加载中,请稍后...".format(f"{index}/{dataframe.shape[0] - 1}", row.iloc[0])
            load_repository.progress(1/(dataframe.shape[0] - 1)*index, text=progress_text)
            time.sleep(4)
            callback(index, row)
        time.sleep(1)
        load_repository.empty()