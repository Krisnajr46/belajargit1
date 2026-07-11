"""Unit test engine. Jalankan: python tests/test_recommender.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from src.preprocessing import build_content
from src.recommender import ContentBasedRecommender


def _sample_df():
    return pd.DataFrame({
        "product_id": [1, 2, 3, 4],
        "product_name": ["Kaos Polos Katun Pria", "Kaos Oblong Katun Pria",
                          "Blender Portable Dapur", "Rice Cooker Mini Dapur"],
        "category": ["Fashion Pria", "Fashion Pria", "Peralatan Rumah", "Peralatan Rumah"],
        "brand": ["Erigo", "Uniqlo", "Cosmos", "Miyako"],
        "description": ["kaos katun adem nyaman", "kaos katun lembut harian",
                        "blender praktis dapur", "rice cooker hemat listrik dapur"],
    })


def test_similar_category():
    df = build_content(_sample_df())
    rec = ContentBasedRecommender(df)
    out = rec.recommend(1, top_n=1)
    assert len(out) == 1
    assert out.iloc[0]["product_id"] == 2
    print("OK test_similar_category")


def test_excludes_self():
    df = build_content(_sample_df())
    rec = ContentBasedRecommender(df)
    out = rec.recommend(1, top_n=None)
    assert 1 not in out["product_id"].tolist()
    print("OK test_excludes_self")


if __name__ == "__main__":
    test_similar_category()
    test_excludes_self()
    print("Semua test lolos")
