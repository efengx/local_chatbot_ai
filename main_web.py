# Human operation
import streamlit as st
from st_pages import Page, show_pages, add_page_title


# 多页应用程序：入口页
st.set_page_config(
    page_title="rjxai",
    page_icon="👋",
)

add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("src/webui/chat_ai.py", "聊天客服", "📞"),
        Page("src/webui/data_repository.py", "知识库", "🗂️"),
    ]
)