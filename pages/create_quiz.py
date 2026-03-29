import io
from pathlib import Path
import streamlit as st
from PIL import Image
import numpy as np
from rembg import remove

st.set_page_config(page_title="問題作成")
st.title("問題作成")

uploaded = st.file_uploader(
    "画像をアップロードしてください",
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded:
    #画像のバイト列に変換したのを格納
    input_bytes = uploaded.getvalue()

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
            st.subheader("背景削除後")
            st.image(result_image, use_container_width=True)

    # ダウンロード用
    download_bytes = io.BytesIO()
    result_image.save(download_bytes, format="PNG")
    download_bytes = download_bytes.getvalue()
    
    base_name = Path(uploaded.name).stem
    download_name = f"{base_name}_removed_bg.png"

    st.download_button(
        label="背景削除画像をダウンロード",
        data=download_bytes,
        file_name=download_name,
        mime="image/png",
    )

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")
