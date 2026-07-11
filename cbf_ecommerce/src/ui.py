"""Komponen tampilan Streamlit (upgrade)."""
import pandas as pd
import streamlit as st
from config import (APP_NAME, APP_TAGLINE, BRAND_COL, CATEGORY_COL, DEFAULT_TOP_N,
                    MARKETPLACE_COL, MAX_TOP_N, NAME_COL, PRICE_COL, PRICE_COLOR,
                    PRIMARY_COLOR, RATING_COL, SECONDARY_COLOR, SOLD_COL)
from src.utils import (category_emoji, format_number, format_rupiah, format_sold,
                       marketplace_color, render_stars)


def inject_css():
    st.markdown("""
    <style>
    .block-container {padding-top: 1.5rem; max-width: 1200px;}
    #MainMenu, footer {visibility: hidden;}
    .rb-hero {background: linear-gradient(135deg,#6C5CE7 0%,#A29BFE 100%);
        border-radius:22px; padding:30px 34px; color:#fff;
        box-shadow:0 10px 30px rgba(108,92,231,0.35); margin-bottom:20px;}
    .rb-hero h1 {font-size:30px; margin:0 0 6px 0; font-weight:800;}
    .rb-hero p {font-size:15px; margin:0; opacity:0.95;}
    .rb-metric {background:#fff; border:1px solid #eee; border-radius:16px;
        padding:16px 18px; box-shadow:0 4px 14px rgba(0,0,0,0.05); text-align:center;}
    .rb-metric .ic {font-size:24px;}
    .rb-metric .val {font-size:22px; font-weight:800; color:#2d3436;}
    .rb-metric .lbl {font-size:12px; color:#636e72; margin-top:2px;}
    .rb-section {font-size:20px; font-weight:800; color:#2d3436; margin:22px 0 12px 0;}
    div[data-testid="stSidebar"] {background:#faf9ff;}
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("<div class='rb-hero'><h1>\U0001F6D2 " + APP_NAME +
                "</h1><p>" + APP_TAGLINE + "</p></div>", unsafe_allow_html=True)


def _metric_html(icon, value, label):
    return ("<div class='rb-metric'><div class='ic'>" + icon + "</div><div class='val'>" +
            value + "</div><div class='lbl'>" + label + "</div></div>")


def render_metrics(df):
    total = len(df)
    avg_rating = df[RATING_COL].mean() if RATING_COL in df.columns else 0
    total_sold = int(df[SOLD_COL].sum()) if SOLD_COL in df.columns else 0
    n_cat = df[CATEGORY_COL].nunique() if CATEGORY_COL in df.columns else 0
    items = [("\U0001F6D2", format_number(total), "Total Produk"),
             ("\u2B50", format(avg_rating, ".2f"), "Rata-rata Rating"),
             ("\U0001F4E6", format_number(total_sold), "Total Terjual"),
             ("\U0001F5C2\uFE0F", str(n_cat), "Kategori")]
    cols = st.columns(4)
    for col, (icon, val, lbl) in zip(cols, items):
        col.markdown(_metric_html(icon, val, lbl), unsafe_allow_html=True)


def render_sidebar_data_source(load_products, load_uploaded_products):
    st.sidebar.markdown("## \u2699\uFE0F " + APP_NAME)
    st.sidebar.markdown("#### \U0001F4C1 Sumber Data")
    uploaded = st.sidebar.file_uploader("Unggah dataset produk (CSV)", type=["csv"])
    if uploaded is not None:
        df = load_uploaded_products(uploaded)
        st.sidebar.success("Memakai: " + uploaded.name)
        return df, "upload::" + uploaded.name + "::" + str(getattr(uploaded, "size", 0))
    df = load_products()
    st.sidebar.caption("Memakai dataset bawaan aplikasi.")
    return df, "default"


def render_sidebar_filters(df):
    st.sidebar.markdown("#### \U0001F39B\uFE0F Filter Rekomendasi")
    top_n = st.sidebar.slider("Jumlah rekomendasi", 3, MAX_TOP_N, DEFAULT_TOP_N)
    cats = sorted(df[CATEGORY_COL].dropna().unique()) if CATEGORY_COL in df.columns else []
    sel_cats = st.sidebar.multiselect("Kategori", cats)
    if MARKETPLACE_COL in df.columns:
        mps = sorted(x for x in df[MARKETPLACE_COL].dropna().unique() if x != "-")
        sel_mps = st.sidebar.multiselect("Marketplace", mps)
    else:
        sel_mps = []
    price = None
    if PRICE_COL in df.columns and len(df):
        pmin, pmax = int(df[PRICE_COL].min()), int(df[PRICE_COL].max())
        if pmin < pmax:
            price = st.sidebar.slider("Rentang harga (Rp)", pmin, pmax, (pmin, pmax), step=1000)
    return {"top_n": top_n, "categories": sel_cats, "marketplaces": sel_mps, "price": price}


def apply_filters(results, filters):
    df = results
    if filters.get("categories"):
        df = df[df[CATEGORY_COL].isin(filters["categories"])]
    if filters.get("marketplaces") and MARKETPLACE_COL in df.columns:
        df = df[df[MARKETPLACE_COL].isin(filters["marketplaces"])]
    price = filters.get("price")
    if price and PRICE_COL in df.columns:
        df = df[(df[PRICE_COL] >= price[0]) & (df[PRICE_COL] <= price[1])]
    return df


def _badge(text, color):
    return ("<span style='background:" + color + ";color:#fff;padding:2px 9px;"
            "border-radius:999px;font-size:11px;font-weight:700;'>" + text + "</span>")


def _card_html(row, similarity=None):
    emoji = category_emoji(row.get(CATEGORY_COL, ""))
    name = str(row.get(NAME_COL, "-"))
    brand = str(row.get(BRAND_COL, "-"))
    price = format_rupiah(row.get(PRICE_COL, 0))
    mp = str(row.get(MARKETPLACE_COL, "-"))
    rating = row.get(RATING_COL, 0)
    sold = format_sold(row.get(SOLD_COL, 0))
    stars = render_stars(rating)
    sim = ""
    if similarity is not None:
        sim = ("<div style='position:absolute;top:10px;right:10px;background:"
               "linear-gradient(135deg," + PRIMARY_COLOR + "," + SECONDARY_COLOR + ");"
               "color:#fff;padding:3px 10px;border-radius:999px;font-size:11px;"
               "font-weight:800;'>\U0001F3AF " + format(similarity * 100, ".0f") + "%</div>")
    mp_badge = _badge(mp, marketplace_color(mp)) if mp != "-" else ""
    return ("<div style='position:relative;background:#fff;border:1px solid #eee;"
            "border-radius:16px;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,0.06);"
            "margin-bottom:16px;'>" + sim +
            "<div style='height:120px;display:flex;align-items:center;justify-content:center;"
            "font-size:56px;background:linear-gradient(135deg,#f6f5ff,#eef0ff);'>" + emoji + "</div>"
            "<div style='padding:12px 14px 16px;'>"
            "<div style='font-weight:700;font-size:14px;line-height:1.3;height:38px;"
            "overflow:hidden;color:#2d3436;'>" + name + "</div>"
            "<div style='margin:7px 0;'>" + mp_badge +
            " <span style='color:#636e72;font-size:12px;'>\u00B7 " + brand + "</span></div>"
            "<div style='color:" + PRICE_COLOR + ";font-weight:800;font-size:16px;'>" + price + "</div>"
            "<div style='color:#f5a623;font-size:13px;margin-top:4px;'>" + stars +
            " <span style='color:#636e72;'>" + str(rating) + "</span></div>"
            "<div style='color:#636e72;font-size:12px;margin-top:2px;'>" + sold + "</div>"
            "</div></div>")


def render_selected_product(row):
    st.markdown("<div class='rb-section'>\U0001F3AF Produk Acuan</div>", unsafe_allow_html=True)
    emoji = category_emoji(row.get(CATEGORY_COL, ""))
    name = str(row.get(NAME_COL, "-"))
    brand = str(row.get(BRAND_COL, "-"))
    cat = str(row.get(CATEGORY_COL, "-"))
    price = format_rupiah(row.get(PRICE_COL, 0))
    mp = str(row.get(MARKETPLACE_COL, "-"))
    rating = row.get(RATING_COL, 0)
    sold = format_sold(row.get(SOLD_COL, 0))
    stars = render_stars(rating)
    mp_badge = _badge(mp, marketplace_color(mp)) if mp != "-" else ""
    st.markdown(
        "<div style='display:flex;gap:20px;background:#fff;border:1px solid #eee;"
        "border-radius:18px;padding:18px 20px;box-shadow:0 6px 18px rgba(0,0,0,0.06);"
        "align-items:center;'>"
        "<div style='min-width:110px;height:110px;border-radius:14px;display:flex;"
        "align-items:center;justify-content:center;font-size:60px;"
        "background:linear-gradient(135deg,#f6f5ff,#eef0ff);'>" + emoji + "</div>"
        "<div style='flex:1;'>"
        "<div style='font-size:18px;font-weight:800;color:#2d3436;'>" + name + "</div>"
        "<div style='margin:8px 0;'>" + mp_badge + " " + _badge(cat, PRIMARY_COLOR) +
        " <span style='color:#636e72;font-size:13px;'>\u00B7 " + brand + "</span></div>"
        "<div style='color:" + PRICE_COLOR + ";font-weight:800;font-size:22px;'>" + price + "</div>"
        "<div style='color:#f5a623;font-size:15px;margin-top:6px;'>" + stars +
        " <span style='color:#636e72;'>" + str(rating) + " \u00B7 " + sold + "</span></div>"
        "</div></div>", unsafe_allow_html=True)


def render_recommendations(results, per_row=3):
    st.markdown("<div class='rb-section'>\u2728 Rekomendasi Produk Serupa</div>", unsafe_allow_html=True)
    if results is None or results.empty:
        st.info("Tidak ada produk yang cocok dengan filter. Longgarkan filter di sidebar.")
        return
    records = results.to_dict("records")
    for i in range(0, len(records), per_row):
        cols = st.columns(per_row)
        for col, rec in zip(cols, records[i:i + per_row]):
            with col:
                st.markdown(_card_html(rec, rec.get("similarity")), unsafe_allow_html=True)


def render_similarity_chart(results):
    if results is None or results.empty:
        return
    st.markdown("<div class='rb-section'>\U0001F4CA Skor Kemiripan</div>", unsafe_allow_html=True)
    chart = results.copy()
    chart["Kemiripan (%)"] = (chart["similarity"] * 100).round(1)
    chart = chart.set_index(NAME_COL)[["Kemiripan (%)"]]
    st.bar_chart(chart, color=PRIMARY_COLOR)


def render_footer():
    st.markdown("<hr style='margin-top:30px;border:none;border-top:1px solid #eee;'>"
                "<div style='text-align:center;color:#b2bec3;font-size:12px;'>" + APP_NAME +
                " \u00B7 Content-Based Filtering (TF-IDF + Cosine Similarity) \u00B7 "
                "Python & Streamlit</div>", unsafe_allow_html=True)
