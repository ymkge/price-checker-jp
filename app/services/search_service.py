import asyncio
from typing import List

from app.models.product import Product
from app.adapters.rakuten import RakutenAdapter
from app.analyzer.review_analyzer import analyze_product_reviews
from app.scrapers.rakuten_scraper import scrape_reviews


async def search_and_analyze(query: str) -> List[Product]:
    """
    商品を検索し、レビューをスクレイピングで取得・分析して結果を返す。
    """
    # 1. アダプターで商品リストを取得
    rakuten_adapter = RakutenAdapter()
    products = await rakuten_adapter.search_products(query)

    # 2. 各商品のレビューを並行してスクレイピング
    async def fetch_and_set_reviews(product: Product):
        """非同期でレビューを取得し、productオブジェクトにセットする内部関数"""
        # スクレイピングでレビュー本文を取得
        # 商品URLがない場合はスキップ
        if not product.url:
            return
        
        scraped_reviews = await scrape_reviews(product.url)
        if scraped_reviews:
            # 取得したレビューで既存のreviewsリストを上書き
            product.reviews = scraped_reviews

    # asyncio.gatherで並列実行し、処理時間を短縮
    await asyncio.gather(*(fetch_and_set_reviews(p) for p in products))

    # 3. 分析処理
    # レビュー本文がセットされたので、感情分析が機能するようになる
    analyzed_products: List[Product] = [
        analyze_product_reviews(p) for p in products
    ]

    return analyzed_products
