import os
import httpx
from typing import List
from dotenv import load_dotenv

from app.models.product import Product, Review
from app.adapters.base import BaseShopAdapter

# .envファイルから環境変数を読み込む
load_dotenv()

RAKUTEN_ITEM_SEARCH_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"


class RakutenAdapter(BaseShopAdapter):
    """
    楽天商品検索APIと通信するためのアダプター。
    """
    def __init__(self):
        self.application_id = os.getenv("RAKUTEN_APP_ID")
        if not self.application_id or self.application_id == "YOUR_RAKUTEN_APP_ID_HERE":
            raise ValueError("RAKUTEN_APP_IDが設定されていません。.envファイルを確認してください。")

    async def search_products(self, query: str) -> List[Product]:
        """
        楽天商品検索APIを叩いて商品情報を取得し、共通Productモデルのリストを返す。
        """
        params = {
            "applicationId": self.application_id,
            "format": "json",
            "keyword": query,
            "hits": 10,  # 取得件数を10件に制限
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(RAKUTEN_ITEM_SEARCH_API_URL, params=params)
            response.raise_for_status()  # エラーがあれば例外を発生させる

        api_response = response.json()
        products: List[Product] = []

        for item in api_response.get("Items", []):
            item_info = item["Item"]
            
            # 楽天APIの評価は5段階評価なので、100点満点に変換する
            review_score = float(item_info.get("reviewAverage", 0)) * 20

            products.append(
                Product(
                    name=item_info.get("itemName", ""),
                    price=float(item_info.get("itemPrice", 0)),
                    url=item_info.get("itemUrl", ""),
                    # APIレスポンスにはレビュー本文がないため、スコアのみをReviewモデルに格納
                    reviews=[
                        Review(text="", score=review_score)
                    ],
                    # Productモデルのanalysis_scoreには、代表値として評価平均を格納
                    analysis_score=review_score
                )
            )
        
        return products
