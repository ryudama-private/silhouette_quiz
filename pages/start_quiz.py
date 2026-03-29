import base64
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="問題開始")
st.title("問題開始")

if "quiz_image_bytes" not in st.session_state:
    st.session_state.quiz_image_bytes = None
if "quiz_image_name" not in st.session_state:
    st.session_state.quiz_image_name = None
if "quiz_deleted" not in st.session_state:
    st.session_state.quiz_deleted = False

if st.session_state.quiz_deleted:
    # 削除済みフラグが立っているときにlocalStorageを消去する
    streamlit_js_eval(
        js_expressions='localStorage.removeItem("silhouette_quiz_image_b64"); localStorage.removeItem("silhouette_quiz_name"); true;',
        key="cleanup_quiz_storage",
    )
elif st.session_state.quiz_image_bytes is None:
    stored_image_b64 = streamlit_js_eval(
        js_expressions='localStorage.getItem("silhouette_quiz_image_b64")',
        key="get_quiz_image_b64",
    )
    stored_name = streamlit_js_eval(
        js_expressions='localStorage.getItem("silhouette_quiz_name")',
        key="get_quiz_name",
    )

    if stored_image_b64:
        try:
            st.session_state.quiz_image_bytes = base64.b64decode(stored_image_b64)
            st.session_state.quiz_image_name = stored_name or "quiz_image"
        except Exception:
            st.warning("保存済みデータの読み込みに失敗しました。問題作成ページで再設定してください。")

quiz_image_bytes = st.session_state.get("quiz_image_bytes")
quiz_image_name = st.session_state.get("quiz_image_name")

if quiz_image_bytes:
    st.subheader("シルエットクイズ")
    st.image(quiz_image_bytes, use_container_width=True)

    user_answer = st.text_input("このシルエットの名前を入力")
    if st.button("回答する"):
        if user_answer.strip().lower() == (quiz_image_name or "").strip().lower():
            st.success("正解です！")
        else:
            st.error("不正解です")
else:
    st.info("まだクイズ画像が設定されていません。問題作成ページで「この画像をクイズに設定」を押してください。")

if quiz_image_bytes and st.button("保存済みクイズ画像を削除"):
    st.session_state.quiz_image_bytes = None
    st.session_state.quiz_image_name = None
    st.session_state.quiz_deleted = True
    st.rerun()

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")
