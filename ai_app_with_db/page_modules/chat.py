import streamlit as st
import ollama
from utils.db import get_connection

def chat_page():
    if "user_id" not in st.session_state:
        st.warning("请先登录")
        st.stop()

    st.title("AI 对话")

    with st.sidebar:
        st.write(f"当前用户：{st.session_state.username}")
        model_name = st.selectbox("选择模型", ["qwen2.5:0.5b", "qwen2.5:7b", "qwen3.5:9b"], index=0)
        if st.button("清空对话"):
            st.session_state.messages = []
            st.rerun()

        if st.button("导出本次对话"):
            if st.session_state.messages:
                content = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                st.download_button(
                    label="下载对话记录",
                    data=content,
                    file_name=f"chat_{st.session_state.username}.txt",
                    mime="text/plain"
                )
            else:
                st.warning("没有对话记录可导出")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("请输入你的问题")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        conn = get_connection()
        conn.execute(
            "INSERT INTO messages (user_id, role, content, model) VALUES (?, ?, ?, ?)",
            (st.session_state.user_id, "user", prompt, model_name)
        )
        conn.commit()

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_reply = ""
            stream = ollama.chat(model=model_name, messages=st.session_state.messages, stream=True)
            for chunk in stream:
                if "message" in chunk and "content" in chunk["message"]:
                    full_reply += chunk["message"]["content"]
                    placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)

        reply = full_reply
        st.session_state.messages.append({"role": "assistant", "content": reply})

        conn.execute(
            "INSERT INTO messages (user_id, role, content, model) VALUES (?, ?, ?, ?)",
            (st.session_state.user_id, "assistant", reply, model_name)
        )
        conn.commit()
        conn.close()