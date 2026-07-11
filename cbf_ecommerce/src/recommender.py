"""Engine Content-Based Filtering (TF-IDF + Cosine Similarity)."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import ID_COL, NAME_COL, TFIDF_PARAMS


class ContentBasedRecommender:
    def __init__(self, df):
        if "content" not in df.columns:
            raise ValueError("DataFrame harus memiliki kolom 'content'.")
        self.df = df.reset_index(drop=True)
        self._vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
        self._matrix = self._vectorizer.fit_transform(self.df["content"])
        self._index_by_id = {pid: pos for pos, pid in enumerate(self.df[ID_COL].tolist())}

    def recommend(self, product_id, top_n=5):
        if product_id not in self._index_by_id:
            raise KeyError("Produk id '" + str(product_id) + "' tidak ditemukan.")
        idx = self._index_by_id[product_id]
        scores = cosine_similarity(self._matrix[idx], self._matrix).ravel()
        result = self.df.copy()
        result["similarity"] = scores
        result = result[result[ID_COL] != product_id]
        result = result.sort_values("similarity", ascending=False)
        if top_n is not None:
            result = result.head(top_n)
        return result.reset_index(drop=True)

    def product_choices(self):
        return {str(row[NAME_COL]) + " (#" + str(row[ID_COL]) + ")": row[ID_COL]
                for _, row in self.df.iterrows()}
