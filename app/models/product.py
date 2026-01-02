from typing import List, Optional
from pydantic import BaseModel, Field


class Review(BaseModel):
    """レビュー情報を格納するモデル"""
    text: str
    score: float


class Product(BaseModel):
    """商品情報を格納する共通モデル"""
    name: str = Field(..., description="商品名")
    price: float = Field(..., description="価格")
    url: str = Field(..., description="商品ページのURL")
    reviews: List[Review] = Field([], description="レビューのリスト")
    analysis_score: Optional[float] = Field(None, description="レビューの総合分析スコア")

