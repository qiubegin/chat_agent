import streamlit as st
from utils.db import get_connection
from utils.auth import verify_password

def login_page():
    st.title("用户登录")
    st.divider()

    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    col1, col2 = st.columns(2)
    with col1:
        login_btn = st.button("登录", use_container_width=True)
    with col2:
        register_btn = st.button("去注册", use_container_width=True)

    if login_btn:
        if not username or not password:
            st.warning("请填写用户名和密码")
        else:
            conn = get_connection()
            cursor = conn.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()
            conn.close()

            if user and verify_password(password, user[2]):
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.page = "chat"
                st.rerun()
            else:
                st.error("用户名或密码错误")

    if register_btn:
        st.session_state.page = "register"
        st.rerun()