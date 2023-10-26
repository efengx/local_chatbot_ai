import streamlit as st
import time
import numpy as np
from src.webui.session import Data
import pandas as pd

st.set_page_config(
    page_title="知识库", 
    page_icon="🗂️",
    layout="wide"
)

st.markdown("# Plotting Demo")



Data.getStorageList()
