"""RekomBelanja - entry point Streamlit. Jalankan: streamlit run app.py"""
import streamlit as st
from config import APP_ICON, APP_TITLE, ID_COL, NAME_COL
from src import ui
from src.data_loader import load_products, load_uploaded_products
from src.services import get_recommender

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide",
                   initial_sidebar_state="expanded")
ui.inject_css()

try:
    df, cache_key = ui.render_sidebar_data_source(load_products, load_uploaded_products)
except Exception as exc:
    st.error("Gagal memuat dataset: " + str(exc))
    st.stop()

ui.render_header()
ui.render_metrics(df)
filters = ui.render_sidebar_filters(df)
recommender = get_recommender(df, cache_key)

# >>> PERBAIKAN: filter juga diterapkan ke daftar produk acuan <<<
browse_df = ui.apply_filters(df, filters)

st.markdown("<div class='rb-section'>🔎 Pilih Produk Acuan</div>", unsafe_allow_html=True)
if browse_df.empty:
    st.warning("Tidak ada produk yang cocok dengan filter. Longgarkan filter di sidebar.")
    st.stop()

choices = {f"{row[NAME_COL]} (#{row[ID_COL]})": row[ID_COL]
           for _, row in browse_df.iterrows()}
label = st.selectbox("Cari & pilih produk", list(choices.keys()),
                     label_visibility="collapsed")
product_id = choices[label]

selected_rows = df[df[ID_COL] == product_id]
if selected_rows.empty:
    st.warning("Produk tidak ditemukan.")
    st.stop()
ui.render_selected_product(selected_rows.iloc[0])

results = recommender.recommend(product_id, top_n=None)
results = ui.apply_filters(results, filters)
results = results.head(filters["top_n"])
ui.render_recommendations(results)
ui.render_similarity_chart(results)
ui.render_footer()