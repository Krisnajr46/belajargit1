"""Konfigurasi terpusat aplikasi."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "products.csv"

ID_COL = "product_id"
NAME_COL = "product_name"
CATEGORY_COL = "category"
BRAND_COL = "brand"
DESC_COL = "description"
PRICE_COL = "price"
MARKETPLACE_COL = "marketplace"
RATING_COL = "rating"
SOLD_COL = "terjual"
DATE_COL = "tanggal_upload"

CONTENT_COLUMNS = [NAME_COL, CATEGORY_COL, BRAND_COL, DESC_COL]

OPTIONAL_COLUMNS = {
    MARKETPLACE_COL: "-",
    RATING_COL: 0.0,
    SOLD_COL: 0,
    DATE_COL: "",
}

DEFAULT_TOP_N = 6
MAX_TOP_N = 12

TFIDF_PARAMS = {"stop_words": "english", "ngram_range": (1, 2), "min_df": 1}

APP_NAME = "RekomBelanja"
APP_TITLE = "RekomBelanja - Rekomendasi Produk E-Commerce"
APP_ICON = "\U0001F6CD\uFE0F"
APP_TAGLINE = "Temukan produk serupa dari Shopee, Tokopedia & TikTok Shop"

PRIMARY_COLOR = "#6C5CE7"
SECONDARY_COLOR = "#A29BFE"
PRICE_COLOR = "#E1493B"

MARKETPLACE_COLORS = {"Shopee": "#EE4D2D", "Tokopedia": "#42B549", "TikTok Shop": "#111111"}

CATEGORY_EMOJI = {
    "Fashion Pria": "\U0001F455",
    "Fashion Wanita": "\U0001F457",
    "Skincare & Kecantikan": "\U0001F484",
    "Gadget & Aksesoris HP": "\U0001F4F1",
    "Peralatan Rumah": "\U0001F3E0",
    "Ibu & Bayi": "\U0001F476",
    "Olahraga & Outdoor": "\u26BD",
    "Makanan & Minuman": "\U0001F36B",
}
DEFAULT_EMOJI = "\U0001F6D2"
