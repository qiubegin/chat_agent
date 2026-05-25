import streamlit as st
import pandas as pd
from utils.db import get_connection


def history_page():
    if "user_id" not in st.session_state:
        st.warning("请先登录")
        st.stop()

    st.title("聊天历史记录")

    # 分页参数
    page_size = st.selectbox("每页显示条数", [10, 20, 50], index=0, key="history_page_size")

    # 获取总记录数
    conn = get_connection()
    cursor = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE user_id = ?",
        (st.session_state.user_id,)
    )
    total_rows = cursor.fetchone()[0]
    conn.close()

    if total_rows == 0:
        st.info("暂无聊天记录")
        return

    # 计算总页数
    total_pages = (total_rows + page_size - 1) // page_size

    # 当前页码
    if "history_page" not in st.session_state:
        st.session_state.history_page = 1

    # 页码选择器
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("上一页", disabled=(st.session_state.history_page == 1)):
            st.session_state.history_page -= 1
            st.rerun()
    with col2:
        st.write(f"第 {st.session_state.history_page} 页 / 共 {total_pages} 页")
    with col3:
        if st.button("下一页", disabled=(st.session_state.history_page == total_pages)):
            st.session_state.history_page += 1
            st.rerun()

    # 计算 OFFSET
    offset = (st.session_state.history_page - 1) * page_size

    # 查询当前页数据
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT datetime(created_at, 'localtime') as 时间, role, content, model
        FROM messages
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', conn, params=(st.session_state.user_id, page_size, offset))
    conn.close()

    st.dataframe(df, use_container_width=True)