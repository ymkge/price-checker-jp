from typing import List
from collections import Counter

from janome.tokenizer import Tokenizer

from app.models.product import Product, Review

# シンプルな感情辞書
POSITIVE_WORDS = ["良い", "最高", "満足", "素晴らしい", "便利", "速い", "きれい", "美しい", "簡単", "嬉しい"]
NEGATIVE_WORDS = ["悪い", "最悪", "不満", "ひどい", "残念", "遅い", "汚い", "壊れ", "難しい", "悲しい"]

def analyze_sentiment(text: str) -> float:
    """
    レビュー本文を形態素解析し、0〜100の感情スコアを算出する。
    スコア50を中間点とする。
    """
    if not text:
        return 50.0

    t = Tokenizer()
    tokens = t.tokenize(text, stream=True)
    
    score = 50.0
    
    for token in tokens:
        base_form = token.base_form
        # 形容詞、動詞、名詞を評価対象とする
        if "形容詞" in token.part_of_speech or "動詞" in token.part_of_speech or "名詞" in token.part_of_speech:
            if base_form in POSITIVE_WORDS:
                score += 5
            elif base_form in NEGATIVE_WORDS:
                score -= 5
    
    # 0〜100の範囲にスコアを収める
    final_score = max(0, min(100, score))
    return final_score

def summarize_reviews(reviews: List[Review]) -> List[str]:
    """
    レビュー群から特徴的なキーワード（名詞）を抽出する。（モック実装）
    """
    t = Tokenizer()
    all_nouns = []
    for review in reviews:
        if not review.text:
            continue
        tokens = t.tokenize(review.text, stream=True)
        nouns = [token.base_form for token in tokens if "名詞" in token.part_of_speech and "一般" in token.part_of_speech]
        all_nouns.extend(nouns)
    
    # 頻出する名詞の上位5件を返す
    counter = Counter(all_nouns)
    return [word for word, count in counter.most_common(5)]


def analyze_product_reviews(product: Product) -> Product:
    """
    Productオブジェクトに含まれる全レビューを分析し、
    各レビューのスコアと製品全体の分析スコアを更新する。
    """
    if not product.reviews:
        product.analysis_score = None
        return product

    total_score = 0
    analyzed_reviews_count = 0

    for review in product.reviews:
        # テキストがあるレビューのみ分析
        if review.text:
            review.score = analyze_sentiment(review.text)
            total_score += review.score
            analyzed_reviews_count += 1

    if analyzed_reviews_count > 0:
        product.analysis_score = total_score / analyzed_reviews_count
    
    return product
