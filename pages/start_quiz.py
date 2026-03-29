import streamlit as st

st.set_page_config(page_title="問題開始")
st.title("問題開始")

quiz_image_bytes = st.session_state.get("quiz_image_bytes")
quiz_image_name = st.session_state.get("quiz_image_name")

if quiz_image_bytes:
    st.subheader("シルエットクイズ")
    st.image(quiz_image_bytes, use_container_width=True)
    st.caption(f"画像名: {quiz_image_name}")
else:
    st.info("まだクイズ画像が設定されていません。問題作成ページで「この画像をクイズに設定」を押してください。")

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")
