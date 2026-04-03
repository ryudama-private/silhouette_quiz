import base64
import json
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="問題開始")
st.title("問題開始")

if "quiz_image_bytes" not in st.session_state:
    st.session_state.quiz_image_bytes = None
if "quiz_image_name" not in st.session_state:
    st.session_state.quiz_image_name = None
if "quiz_original_bytes" not in st.session_state:
    st.session_state.quiz_original_bytes = None
if "quiz_revealed" not in st.session_state:
    st.session_state.quiz_revealed = False
if "quiz_items" not in st.session_state:
    st.session_state.quiz_items = []
if "quiz_current_index" not in st.session_state:
    st.session_state.quiz_current_index = 0
if "quiz_items_initialized" not in st.session_state:
    st.session_state.quiz_items_initialized = False

if not st.session_state.quiz_items_initialized:
    stored_items_json = streamlit_js_eval(
        js_expressions='localStorage.getItem("silhouette_quiz_items_json")',
        key="get_quiz_items_json_start",
    )
    if stored_items_json:
        try:
            stored_items = json.loads(stored_items_json)
            if isinstance(stored_items, list):
                st.session_state.quiz_items = [
                    item for item in stored_items
                    if isinstance(item, dict)
                    and item.get("name")
                    and item.get("image_b64")
                ]
        except Exception:
            st.warning("保存済みデータの読み込みに失敗しました。問題作成ページで再設定してください。")
    st.session_state.quiz_items_initialized = True

quiz_items = st.session_state.quiz_items

if quiz_items:
    labels = [f"No.{idx + 1}" for idx, _ in enumerate(quiz_items)]
    max_index = len(quiz_items) - 1
    if st.session_state.quiz_current_index > max_index:
        st.session_state.quiz_current_index = max_index

    selected_label = st.selectbox(
        "出題する問題を選択",
        labels,
        index=st.session_state.quiz_current_index,
    )
    selected_index = labels.index(selected_label)
    if selected_index != st.session_state.quiz_current_index:
        st.session_state.quiz_current_index = selected_index
        st.session_state.quiz_revealed = False
        st.rerun()

    current = quiz_items[st.session_state.quiz_current_index]
    quiz_image_bytes = base64.b64decode(current["image_b64"])
    quiz_original_bytes = base64.b64decode(current["original_b64"]) if current.get("original_b64") else None
    quiz_image_name = current.get("name", "")

    display_bytes = quiz_image_bytes
    if st.session_state.quiz_revealed and quiz_original_bytes:
        display_bytes = quiz_original_bytes

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.image(display_bytes, use_container_width=True)

    if not st.session_state.quiz_revealed:
        user_answer = st.text_input("このシルエットの名前を入力")
        if st.button("回答する"):
            if user_answer.strip().lower() == quiz_image_name.strip().lower():
                st.session_state.quiz_revealed = True
                st.rerun()
            else:
                st.error("不正解です。もう一度挑戦してください。")
    else:
        st.success(f"正解です: {quiz_image_name}")

    if st.button("選択中の問題を削除"):
        del st.session_state.quiz_items[st.session_state.quiz_current_index]
        if st.session_state.quiz_current_index >= len(st.session_state.quiz_items):
            st.session_state.quiz_current_index = max(0, len(st.session_state.quiz_items) - 1)
        st.session_state.quiz_revealed = False

        if st.session_state.quiz_items:
            items_json = json.dumps(st.session_state.quiz_items, ensure_ascii=False)
            streamlit_js_eval(
                js_expressions=f'localStorage.setItem("silhouette_quiz_items_json", {json.dumps(items_json, ensure_ascii=False)}); localStorage.removeItem("silhouette_quiz_image_b64"); localStorage.removeItem("silhouette_quiz_name"); localStorage.removeItem("silhouette_quiz_original_b64"); true;',
                key="set_quiz_items_json_after_delete",
            )
        else:
            streamlit_js_eval(
                js_expressions='localStorage.removeItem("silhouette_quiz_items_json"); localStorage.removeItem("silhouette_quiz_image_b64"); localStorage.removeItem("silhouette_quiz_name"); localStorage.removeItem("silhouette_quiz_original_b64"); true;',
                key="remove_quiz_items_json_after_delete",
            )

        if not st.session_state.quiz_items:
            st.session_state.quiz_image_bytes = None
            st.session_state.quiz_image_name = None
            st.session_state.quiz_original_bytes = None

        st.rerun()

    if st.button("すべての問題を削除"):
        st.session_state.quiz_items = []
        st.session_state.quiz_current_index = 0
        st.session_state.quiz_image_bytes = None
        st.session_state.quiz_image_name = None
        st.session_state.quiz_original_bytes = None
        st.session_state.quiz_revealed = False
        st.session_state.quiz_items_initialized = True

        streamlit_js_eval(
            js_expressions='localStorage.removeItem("silhouette_quiz_items_json"); localStorage.removeItem("silhouette_quiz_image_b64"); localStorage.removeItem("silhouette_quiz_name"); localStorage.removeItem("silhouette_quiz_original_b64"); true;',
            key="clear_all_quiz_items",
        )

        st.rerun()
else:
    st.info("まだクイズが登録されていません。問題作成ページで「この画像をクイズに設定」を押してください。")

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")
