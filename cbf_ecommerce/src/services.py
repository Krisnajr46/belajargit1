"""Service: membangun engine dengan cache Streamlit."""
import streamlit as st
from src.recommender import ContentBasedRecommender


@st.cache_resource(show_spinner="Membangun engine rekomendasi (TF-IDF)...")
def get_recommender(_df, cache_key):
    _ = cache_key
    return ContentBasedRecommender(_df)
