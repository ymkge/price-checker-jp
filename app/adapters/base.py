from abc import ABC, abstractmethod
from typing import List
from app.models.product import Product


class BaseShopAdapter(ABC):
    """
    各ECサイトAPIと通信するためのアダプターの抽象基底クラス。
    """

    @abstractmethod
    async def search_products(self, query: str) -> List[Product]:
        """
        指定されたクエリで商品を検索し、Productモデルのリストを返す。

        :param query: 検索キーワード
        :return: Productオブジェクトのリスト
        """
        pass
