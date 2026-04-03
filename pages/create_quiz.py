import io
import time
import base64
import json
import streamlit as st
from PIL import Image
from pathlib import Path
import numpy as np
from rembg import remove
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="問題作成")
st.title("問題作成")

# セッションステートの初期化（ページが置き換わっても保持されるようにしている）
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
if "quiz_items_initialized" not in st.session_state:
    st.session_state.quiz_items_initialized = False

if not st.session_state.quiz_items_initialized:
    stored_items_json = streamlit_js_eval(
        js_expressions='localStorage.getItem("silhouette_quiz_items_json")',
        key="get_quiz_items_json_create",
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
            st.warning("保存済みクイズデータの読み込みに失敗しました。")
    st.session_state.quiz_items_initialized = True

uploaded = st.file_uploader(
    "画像をアップロードしてください",
    type=["png", "jpg", "jpeg", "webp"]
)
st.caption("AIが認識しやすいよう、できるだけ鮮明で、対象が1つだけはっきり写っている画像をおすすめします。")
st.caption("参考例: illustAC の画像ページです。画像の利用条件やライセンスは必ずご自身でご確認ください。")
st.markdown("[画像の例はこちら（illustAC）](https://www.ac-illust.com/main/detail.php?id=26939896&word=%E3%81%8B%E3%82%8F%E3%81%84%E3%81%84%E3%80%80%E6%9F%B4%E7%8A%AC%E3%80%80%E5%BE%85%E3%81%A6%EF%BC%88%E6%AD%A3%E9%9D%A2%EF%BC%89)")

if uploaded:
    #画像のバイト列に変換したのを格納
    input_bytes = uploaded.getvalue()
    
    # 解答名の入力フォーム
    next_no = len(st.session_state.quiz_items) + 1
    file_stem = Path(uploaded.name).stem.strip()
    default_answer = file_stem or f"No.{next_no}"
    answer_input = st.text_input(
        "この問題の解答",
        value=default_answer
    )
    # rembgで背景除去
    output_bytes = remove(input_bytes)  #rembgによって背景除去された画像のバイト列
    removed_image = Image.open(io.BytesIO(output_bytes)).convert('RGBA')    #背景除去後のバイト列を、透明度付きの扱いやすい画像に変換

    # NumPy 配列に変換
    img_array = np.array(removed_image)
    alpha = img_array[:, :, 3]  #透明度を取り出す

    # アルファが高い部分（前景）は黒、低い部分（背景）は青
    blue = (0, 115, 255)  # 青
    black = (0, 0, 0)  # 黒
    
    result_array = np.zeros_like(img_array)
    mask = alpha > 128  # 透明度が128以上の部分を前景とみなす
    
    result_array[mask] = [black[0], black[1], black[2], 255]  # 前景を黒
    result_array[~mask] = [blue[0], blue[1], blue[2], 255]   # 背景を青

    result_image = Image.fromarray(result_array, 'RGBA')

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("元画像")
            st.image(input_bytes, use_container_width=True)
    with col2:
        with st.container(border=True):
            st.subheader("シルエット画像")
            st.image(result_image, use_container_width=True)

    # クイズ保存用（PNGバイト列化）
    download_bytes = io.BytesIO()
    result_image.save(download_bytes, format="PNG")
    download_bytes = download_bytes.getvalue()
    
    answer_name = answer_input.strip() or default_answer

    if st.button("この画像をクイズに設定"):
        if not answer_input.strip():
            st.warning("解答を入力してください")
        else:
            image_b64 = base64.b64encode(download_bytes).decode("utf-8")
            original_b64 = base64.b64encode(input_bytes).decode("utf-8")

            st.session_state.quiz_items.append(
                {
                    "name": answer_name,
                    "image_b64": image_b64,
                    "original_b64": original_b64,
                }
            )

            st.session_state.quiz_image_bytes = download_bytes
            st.session_state.quiz_image_name = answer_name
            st.session_state.quiz_original_bytes = input_bytes
            st.session_state.quiz_revealed = False
            success_msg = st.empty()
            success_msg.success("クイズを追加しました。問題開始ページで確認できます。")
            time.sleep(10)
            success_msg.empty()

            items_json = json.dumps(st.session_state.quiz_items, ensure_ascii=False)
            streamlit_js_eval(
                js_expressions=f'localStorage.setItem("silhouette_quiz_items_json", {json.dumps(items_json, ensure_ascii=False)}); localStorage.removeItem("silhouette_quiz_image_b64"); localStorage.removeItem("silhouette_quiz_name"); localStorage.removeItem("silhouette_quiz_original_b64"); true;',
                key="set_quiz_items_json",
            )

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")
