import streamlit as st
from PIL import Image

st.set_page_config(page_title="問題作成")
st.title("問題作成")

uploaded = st.file_uploader(
"画像をアップロードしてください",
type=["png", "jpg", "jpeg", "webp"]
)

if uploaded is not None:
    img = Image.open(uploaded)
    st.image(img, caption="アップロード画像", use_container_width=True)

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")
