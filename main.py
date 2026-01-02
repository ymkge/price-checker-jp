from fastapi import FastAPI

app = FastAPI(
    title="price-checker-jp",
    description="ECサイトの価格比較・レビュー分析API",
    version="0.1.0",
)

@app.get("/")
async def read_root():
    """
    ルートエンドポイント
    """
    return {"message": "Welcome to price-checker-jp API!"}
