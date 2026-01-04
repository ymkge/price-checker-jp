# price-checker-jp

ECサイトの価格比較・レビュー分析を行うためのバックエンドAPIです。

## 概要

このプロジェクトは、複数のECサイトから商品情報を収集し、価格やレビューを比較・分析するためのバックエンド機能を提供します。現在は楽天商品検索APIで商品情報を取得し、取得した商品ページをスクレイピングすることでレビュー本文を収集します。収集したデータに対し、簡易的な感情分析機能も実装されています。

## 技術スタック

- **言語:** Python 3.10+
- **フレームワーク:** FastAPI
- **主要ライブラリ:**
  - `httpx`: 非同期HTTPクライアント
  - `pydantic`: データバリデーション
  - `python-dotenv`: 環境変数管理
  - `janome`: 日本語形態素解析
  - `beautifulsoup4`, `lxml`: HTMLスクレイピング
  - `uvicorn`: ASGIサーバー

## プロジェクト構造

```
.
├── app
│   ├── adapters
│   │   ├── base.py
│   │   └── rakuten.py
│   ├── analyzer
│   │   └── review_analyzer.py
│   ├── api
│   │   └── search.py
│   ├── models
│   │   └── product.py
│   ├── scrapers
│   │   └── rakuten_scraper.py
│   └── services
│       └── search_service.py
├── .env
├── main.py
├── README.md
└── requirements.txt
```

## セットアップと実行方法

### 1. 依存関係のインストール

プロジェクトのルートディレクトリで以下のコマンドを実行し、必要なライブラリをインストールします。

```bash
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

## APIの使い方

サーバー起動後、以下のエンドポイントが利用可能です。

### 商品検索 (`/search`)

WebブラウザやAPIクライアントから、以下のURLにGETリクエストを送信します。

`http://127.0.0.1:8000/search?keyword=YOUR_KEYWORD`

**例:**
```
http://127.0.0.1:8000/search?keyword=Python
```

成功すると、検索・分析された商品情報のリストがJSON形式で返されます。

### APIドキュメント (`/docs`)

`http://127.0.0.1:8000/docs`

このページでは、APIの仕様を対話的に確認したり、直接リクエストを送信してテストすることができます。

## 実装済みの機能

- FastAPIによるWebサーバーの基本設定
- `Product` や `Review` などの共通データモデル
- **楽天商品検索APIとの連携** (`RakutenAdapter`)
- **商品レビューページのスクレイピングによるレビュー本文取得** (`RakutenScraper`)
- **収集したレビュー本文に基づく日本語感情分析機能** (`ReviewAnalyzer`)
- **検索・スクレイピング・分析を統括するサービスロジック** (`SearchService`)
- **`/search` APIエンドポイントの実装**

## 次のステップ

- スクレイピングの安定化（サイト構造の変更への対応、エラーハンドリング強化）
- Amazonなど、他のECサイト用アダプターの追加（APIベースのものを優先）
- 感情分析ロジックの高度化（感情辞書の拡充など）
- 検索結果を永続化するためのデータベース導入
- フロントエンドアプリケーションとの連携
