import streamlit as st
import pandas as pd
import sqlite3
from utils.db import get_connection
from utils.auth import hash_password

def register_page():
    st.title("用户注册")
    st.divider()

    with st.form("register_form"):
        name = st.text_input("用户名")
        pwd = st.text_input("密码", type="password")
        age = st.number_input("年龄", min_value=0, max_value=120, step=1)
        gender = st.radio("性别", ["男", "女"])
        birthday = st.date_input("出生日期", format="YYYY-MM-DD")
        height = st.slider("身高(cm)", 0, 250, 170)
        submitted = st.form_submit_button("注册")

        if submitted:
            if not name or not pwd:
                st.warning("用户名和密码不能为空")
            else:
                conn = get_connection()
                try:
                    hashed_pwd = hash_password(pwd)
                    conn.execute('''
                        INSERT INTO users (username, password, age, gender, birthday, height)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (name, hashed_pwd, age, gender, birthday.strftime('%Y-%m-%d'), height))
                    conn.commit()
                    st.success("注册成功！请登录")
                    st.session_state.page = "login"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("用户名已存在")
                finally:
                    conn.close()

    st.divider()
    if st.button("查看所有用户"):
        conn = get_connection()
        df = pd.read_sql_query("SELECT id, username, age, gender, birthday, height FROM users", conn)
        st.dataframe(df)
        conn.close()

    st.divider()
    if st.button("已有账号？去登录"):
        st.session_state.page = "login"
        st.rerun()