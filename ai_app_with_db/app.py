import streamlit as st
from utils.db import init_db
from page_modules.login import login_page
from page_modules.register import register_page
from page_modules.chat import chat_page
from page_modules.history import history_page

# st.set_page_config(page_title="AI 应用平台", layout="wide")
st.set_page_config(page_title="AI 应用平台", layout="wide", initial_sidebar_state="expanded")

init_db()

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user_id" not in st.session_state:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
    else:
        st.session_state.page = "login"
        st.rerun()
else:
    with st.sidebar:
        st.write(f"当前用户：{st.session_state.username}")
        if st.button("退出登录"):
            del st.session_state.user_id
            del st.session_state.username
            st.session_state.page = "login"
            st.rerun()
        st.divider()
        page = st.radio("导航", ["AI 对话", "历史记录", "用户注册"], key="main_nav")

    if page == "AI 对话":
        st.session_state.page = "chat"
    elif page == "历史记录":
        st.session_state.page = "history"
    elif page == "用户注册":
        st.session_state.page = "register"

    if st.session_state.page == "chat":
        chat_page()
    elif st.session_state.page == "history":
        history_page()
    elif st.session_state.page == "register":
        register_page()