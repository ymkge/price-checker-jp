# price-checker-jp

ECサイトの価格比較・レビュー分析を行うためのバックエンドAPIです。

## 概要

このプロジェクトは、複数のECサイトから商品情報を収集し、価格やレビューを比較・分析するためのバックエンド機能を提供します。現在は楽天商品検索APIに対応しています。

## 技術スタック

- **言語:** Python 3.10+
- **フレームワーク:** FastAPI
- **主要ライブラリ:**
  - `httpx`: 非同期HTTPクライアント
  - `pydantic`: データバリデーション
  - `python-dotenv`: 環境変数管理
  - `janome`: (導入予定) 日本語形態素解析
  - `uvicorn`: ASGIサーバー

## プロジェクト構造

クリーンアーキテクチャの考え方に基づき、関心事を分離しています。

```
.
├── app
│   ├── adapters      # 外部API（ECサイト）との通信
│   │   ├── base.py
│   │   └── rakuten.py
│   ├── analyzer      # レビュー分析ロジック (未実装)
│   ├── api           # APIエンドポイント (未実装)
│   ├── models        # データ構造の定義
│   │   └── product.py
│   └── services      # ビジネスロジック (未実装)
├── .env              # 環境変数ファイル
├── main.py           # FastAPIアプリケーションのエントリーポイント
├── README.md         # このファイル
└── requirements.txt  # Pythonライブラリの依存関係
```

## セットアップと実行方法

### 1. 依存関係のインストール

```bash
# 仮想環境の作成を推奨
# python -m venv venv
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. 環境変数の設定

プロジェクトルートにある `.env` ファイルを開き、ご自身の楽天アプリケーションIDを設定してください。

```dotenv
RAKUTEN_APP_ID="YOUR_RAKUTEN_APP_ID_HERE"
```

### 3. 開発サーバーの起動

以下のコマンドで、ホットリロード対応の開発サーバーを起動します。

```bash
uvicorn main:app --reload
```

サーバーが起動すると、`http://127.0.0.1:8000` でアクセスできます。
現在はトップページ (`/`) のみアクセス可能です。

## 現在実装済みの機能

- FastAPIによるWebサーバーの基本設定
- 楽天商品検索APIを利用した商品データ（商品名、価格、URL、評価平均）の取得機能 (`RakutenAdapter`)
- `Product` や `Review` などの共通データモデルの定義

## 次のステップ

- レビュー分析機能の実装 (`app/analyzer`)
- 検索機能を外部に公開するためのAPIエンドポイントの実装 (`app/api`)
- 複数ECサイトの検索結果を統合するビジネスロジックの実装 (`app/services`)
