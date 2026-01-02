from typing import List
from fastapi import APIRouter, Query

from app.models.product import Product
from app.services.search_service import search_and_analyze

router = APIRouter(
    prefix="/search",
    tags=["Product Search"],
)

@router.get("/", response_model=List[Product])
async def search_products(
    keyword: str = Query(..., min_length=1, description="検索キーワード")
):
    """
    指定されたキーワードで商品を検索し、レビュー分析結果と共に返します。
    """
    products = await search_and_analyze(keyword)
    return products
