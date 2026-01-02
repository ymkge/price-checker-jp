from fastapi import FastAPI
from app.api import search

app = FastAPI(
    title="price-checker-jp",
    description="ECサイトの価格比較・レビュー分析API",
    version="0.1.0",
)

# /search エンドポイントのルーターを登録
app.include_router(search.router)


@app.get("/")
async def read_root():
    """
    ルートエンドポイント
    """
    return {"message": "Welcome to price-checker-jp API!"}
