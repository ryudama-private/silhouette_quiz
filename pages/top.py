import streamlit as st

st.set_page_config(page_title="トップ")
st.title("シルエットクイズ")

st.write("画像からシルエットクイズを作って遊べるアプリです。")
st.info("※画像の利用にはご注意ください（詳細は下部の免責事項をご確認ください）")

st.subheader("使い方")
st.write("1. 問題作成ページで画像をアップロードしてクイズを設定します。")
st.write("2. 問題開始ページでシルエットを見て答えを入力します。")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/create_quiz.py", label="問題作成へ")
with col2:
    st.page_link("pages/start_quiz.py", label="問題開始へ")
    
    
st.subheader("免責事項")

st.write("・本アプリの利用にあたっては、利用者ご自身の責任において行ってください。")

st.write("・アップロードする画像については、利用者ご自身で著作権・肖像権・その他の権利関係を確認し、適法に利用してください。")
st.write("・第三者の権利を侵害する画像のアップロードは禁止します。これに違反した場合の責任はすべて利用者に帰属します。")

st.write("・シルエット画像の生成にはAIを使用しています。そのため、意図しない結果や不正確なマスキングが発生する場合があります。")

st.warning(
    "重要: 本アプリは Streamlit Community Cloud 上で公開されることを想定しており、"
    "十分なセキュリティ対策や完全な安全性を保証するものではありません。"
    "本アプリの利用、第三者による不正アクセス、踏み台利用、情報漏えい、その他のトラブルにより生じたいかなる損害についても、作者は一切責任を負いません。"
)

st.write("・本アプリの内容は予告なく変更・停止・終了する場合があります。")

st.write("・クイズ画像の情報がブラウザ内に一時的に保存される場合があります。共有端末では利用後に削除してください。")

with st.sidebar:
    st.header("メニュー")
    st.page_link("pages/top.py", label="トップ")
    st.page_link("pages/create_quiz.py", label="問題作成")
    st.page_link("pages/start_quiz.py", label="問題開始")