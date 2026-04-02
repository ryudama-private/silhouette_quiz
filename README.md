# シルエットクイズ

- 画像からシルエットクイズを作成して遊べる Streamlit アプリです。
- アップロードした画像を rembg(Remove Background)で加工し、前景を黒・背景を青に変換したクイズ画像を生成します。

- 公開URL: [Silhouette Quiz](https://silhouettequiz-fprwm6qudqwyw7jvgwhqho.streamlit.app/)
- GitHub: [ryudama-private/silhouette_quiz](https://github.com/ryudama-private/silhouette_quiz)

## 作成の背景

- 友人から、昔のポケモンアニメCM前にあった「だーれだ？」のようなクイズを作ってほしいというリクエストを受けたことがきっかけです。
- 誰でも手軽にシルエットクイズを作って遊べる体験を目指して、このアプリを作成しました。

## 設計の意図

- シルエット化には rembg を採用し、画像処理の知識がなくてもクイズ用シルエットを作れるようにしました。
- データ保存は localStorage を採用し、DB設計の複雑さや公開時の運用コストを抑える構成にしました。

## 特徴

- 画像アップロードからクイズ作成までをブラウザ上で完結
- AI を活用したシルエット画像の自動生成
- 正解時にシルエットから元画像へ切り替え
- クイズデータをブラウザ localStorage に保存(DB不要)
- トップページにチュートリアル動画と更新履歴を表示

## 画面構成

- `app.py`: 起動時にトップページへ遷移
- `pages/top.py`: アプリ説明、使い方、チュートリアル、更新履歴、免責事項
- `pages/create_quiz.py`: 画像アップロード、シルエット生成、クイズ設定
- `pages/start_quiz.py`: クイズ出題、回答判定、保存済みデータ削除

## 使用技術

- Streamlit
- Pillow
- NumPy
- rembg
- onnxruntime
- streamlit-js-eval

依存関係は `requirements.txt` を参照してください。

## セットアップ

1. このリポジトリを取得
2. 仮想環境を作成
3. 依存パッケージをインストール

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 起動方法

```powershell
streamlit run app.py
```

## 使い方

1. トップページから「問題作成」へ移動
2. 画像をアップロードしてシルエットを確認
3. 「この画像をクイズに設定」を押す
4. 「問題開始」で回答を入力
5. 正解すると元画像が表示される

## データ保存について

- クイズ画像・答え名・元画像はブラウザの localStorage に保存されます
- 共有端末で利用した場合は、保存済みクイズ画像を削除してから終了してください

## 注意事項

- 画像の著作権、肖像権、利用許諾は利用者自身で確認してください
- 背景除去は AI 処理のため、意図しないマスキング結果になる場合があります

## 更新履歴

- 2026-03-29: リリース
