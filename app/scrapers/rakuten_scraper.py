import httpx
from typing import List
from bs4 import BeautifulSoup

from app.models.product import Review

# 一般的なブラウザのUser-Agentを設定し、ボット判定を回避する
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

async def scrape_reviews(url: str) -> List[Review]:
    """
    指定された商品URLからレビュー情報をスクレイピングで取得する。

    Args:
        url: 楽天市場の商品ページのURL

    Returns:
        レビュー(Reviewモデル)のリスト。取得できない場合は空のリスト。
    """
    reviews: List[Review] = []
    try:
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
            # タイムアウトを10秒に設定
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()  # HTTPエラーがあれば例外を発生

        soup = BeautifulSoup(response.text, "lxml")

        # レビュー1件ごとのコンテナ要素を取得
        review_items = soup.select("div.revRvwUserEntry_item")

        for item in review_items:
            # レビュー本文のテキストを取得
            comment_element = item.select_one("dd.revRvwUserEntry_comment_text")
            comment_text = comment_element.get_text(strip=True) if comment_element else ""

            # 評価点(星の数)を取得
            rating_element = item.select_one("span.revUserRvwerNum")
            rating_text = rating_element.get_text(strip=True) if rating_element else "0"
            
            try:
                # 評価は5段階評価なので100点満点に変換
                rating_score = float(rating_text) * 20
            except (ValueError, TypeError):
                rating_score = 0.0

            if comment_text:
                reviews.append(
                    Review(
                        text=comment_text,
                        score=rating_score
                    )
                )
        
        return reviews

    except httpx.HTTPStatusError as e:
        print(f"HTTPエラーが発生しました: {e.response.status_code} for url: {url}")
        return []
    except httpx.RequestError as e:
        print(f"リクエストエラーが発生しました: {e} for url: {url}")
        return []
    except Exception as e:
        print(f"スクレイピング中に予期せぬエラーが発生しました: {e} for url: {url}")
        return []
