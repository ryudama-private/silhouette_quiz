import streamlit as st

st.set_page_config(page_title="トップ")
st.title("トップ")

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")