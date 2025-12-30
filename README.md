# price-checker-jp

このプロンプトは、Geminiが「一貫性のある設計」を維持できるように、前提条件・アーキテクチャ・具体的なタスクを構造化して伝えます。

---

### 1. プロジェクト基盤構築プロンプト

ターミナルで最初に打ち込む、プロジェクトの「設計図」と「雛形」を作らせるためのプロンプトです。

```markdown
# Role
あなたはシニアフルスタックエンジニアとして、EC価格比較・レビュー分析アプリ「price-checker-jp」のバックエンド基盤を構築してください。

# Technology Stack
- Framework: FastAPI
- Language: Python 3.10+
- Library: httpx (API通信), pydantic (バリデーション), python-dotenv (環境変数), Janome (日本語解析)

# Architecture
クリーンアーキテクチャの考え方に基づき、以下のディレクトリ構造を作成してください：
- app/api/: ルーティング
- app/adapters/: 各ECサイト(楽天, Amazon)のAPI通信ロジック（BaseAdapterを継承）
- app/services/: ビジネスロジック（複数ショップのデータ統合）
- app/analyzer/: レビューテキストの分析エンジン
- app/models/: 共通データ構造（Pydanticモデル）

# Tasks
1. 上記ディレクトリ構造を自動生成してください。
2. 共通のデータ型を定義する `app/models/product.py` を作成してください（商品名、価格、URL、レビューリスト、分析スコアを含む）。
3. 拡張性を考慮した `app/adapters/base.py` の抽象クラスを作成してください。
4. FastAPIのメインエントリーポイント `main.py` と、ライブラリ管理用の `requirements.txt` を生成してください。

```

---

### 2. 楽天APIアダプター実装プロンプト

基盤ができたら、次は具体的な接続パーツを作らせます。

```markdown
# Context
@app/adapters/base.py と @app/models/product.py を踏まえて実装してください。

# Task
楽天商品検索APIを使用してデータを取得する `app/adapters/rakuten.py` を実装してください。

# Requirements
- BaseShopAdapter を継承し、`search_products` メソッドを実装すること。
- 楽天の Application ID は環境変数 `RAKUTEN_APP_ID` から取得してください。
- レスポンスから「商品名」「価格」「商品URL」「評価点数」を抽出し、共通モデルにマッピングしてください。
- 非同期(async/await)と `httpx` を使用してください。

```

---

### 3. レビュー分析ロジック実装プロンプト

ここがこのアプリの付加価値となる部分です。

```markdown
# Context
取得した商品のレビューリストを分析する機能を追加します。

# Task
`app/analyzer/review_analyzer.py` を作成してください。

# Logic
1. `analyze_sentiment`: Janomeを使用して、レビュー本文からポジティブ・ネガティブなキーワードを抽出し、0〜100のスコアを算出するロジック。
2. `summarize_reviews`: (モックで可) レビュー群から特徴的なキーワードを抽出する。
3. これらの結果を統合して、`app/models/product.py` で定義した分析結果フィールドにセットする関数を実装してください。

```

---

### Gemini CLI での実行のコツ

Gemini CLI（特に Google Cloud の `gcloud ai components` やOSSのツール）を使っている場合、以下の点に注意するとよりスムーズです。

* **コンテキストの共有**: 2回目以降のプロンプトでは、必ず `@app/models/product.py` のように既存ファイルを指定してください。これにより、型定義の不一致を防げます。
* **ステップバイステップ**: 一度に「Amazonも楽天も分析も全部」と頼むより、上記のように「基盤」→「アダプター」→「分析」と分ける方が、コードの品質が高まります。
* **動作確認の依頼**: プロンプトの最後に `「このコードをテストするための pytest 用のスクリプトも書いて」` と付け加えると、テストコードまで自動生成してくれます。

まずは **「1. プロジェクト基盤構築プロンプト」** を実行して、手元にコードを生成させてみるのがおすすめです！

次は、このプロンプトで生成されたコードに対して、**「Amazon APIのモック作成」**や**「フロントエンドとの連携用API作成」**に進みますか？