"""Preprocessing teks untuk TF-IDF."""
import re
import pandas as pd
from config import CONTENT_COLUMNS


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_content(df):
    df = df.copy()
    for col in CONTENT_COLUMNS:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)
    df["content"] = df[CONTENT_COLUMNS].agg(" ".join, axis=1).map(clean_text)
    return df
