from typing import List

from app.models.product import Product
from app.adapters.rakuten import RakutenAdapter
from app.analyzer.review_analyzer import analyze_product_reviews


async def search_and_analyze(query: str) -> List[Product]:
    """
    指定されたクエリで商品を検索し、レビュー分析も行って結果を返すサービス関数。

    1. アダプターを使って外部APIから商品リストを取得する。
    2. 各商品のレビューをアナライザーで分析する。
    3. 分析済みの商品リストを返す。
    """
    # 1. アダプターの初期化とデータ取得
    rakuten_adapter = RakutenAdapter()
    products = await rakuten_adapter.search_products(query)

    # 2. 分析処理
    analyzed_products: List[Product] = []
    for product in products:
        # レビュー分析を実行し、結果をモデルに反映させる
        analyzed_product = analyze_product_reviews(product)
        analyzed_products.append(analyzed_product)

    # 3. 分析済みリストを返す
    return analyzed_products
