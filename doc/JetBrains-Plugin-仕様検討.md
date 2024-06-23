# ソフトウェアの目的
LLMを利用して、コーディングの補助をおこなうアプリ・IDEのPluginを作成する。

# 要望
- ソースコードを実装する際のアシスタントができる
  - TODO,FIXMEの実装
  - コードの説明
  - コメント追加
  - テスト作成
  - コードの改善
  - コードレビュー
- アドバイスしてほしいソースコードを選択できる
- アドバイスの際にほかのファイルを参照できる
  - ソースコードをEmbeddingして、コサイン類似度での検索を可能にする
  - クラス名・関数名などで関連するファイルを参照する
  - 明示的に参照するファイルを指定できる
  - ソースコード以外も参照できるようにする
    - web site
    - pdfファイル
    - 画像ファイル
- 利用料金がわかる
  - Chat/EmbeddingのToken数がわかる
    - Token/料金換算のテーブルを設定できる
- アプリのCore部分はLLMの進化についていきやすくするためPythonを使う
  - Python単独でもコーディング補助のアプリとして利用できる
- IDE の Plugin として利用できる
  - IntelliJ/PyCharmをターゲットとする
    - IntelliJ/PyCharmのPluginの実装言語はkotlin
    - kotlinからPythonを呼び出せるようにするためPython側のCoreはCLIに対応する
    - PluginからはCLIを呼び出す
- 利用するLLMを選択できる
  - OpenAI
  - Amazon Bedrock Claude3
  - Google Gemini Pro
  - Ollama
- 複数のLLMを用いてアンサンブルによる高度な応答にも対応する
