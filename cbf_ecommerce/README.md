# RekomBelanja - Sistem Rekomendasi Produk E-Commerce

Aplikasi web rekomendasi produk berbasis Content-Based Filtering (TF-IDF + Cosine Similarity) dengan tampilan modern. Dibuat dengan Python & Streamlit, bergaya marketplace Indonesia (Shopee, Tokopedia, TikTok Shop).

## Fitur
- Rekomendasi produk serupa + skor kemiripan (persen)
- Kartu produk modern, badge marketplace, rating bintang, harga Rupiah
- Dashboard metrik (total produk, rating, terjual, kategori)
- Filter: kategori, marketplace, rentang harga, jumlah rekomendasi
- Grafik skor kemiripan
- Bisa unggah dataset CSV sendiri

## Struktur
```
cbf_ecommerce/
  app.py
  config.py
  requirements.txt
  data/products.csv
  src/ (preprocessing, data_loader, recommender, services, utils, ui)
  tests/test_recommender.py
```

## Cara Menjalankan
```bash
cd cbf_ecommerce
pip install -r requirements.txt
streamlit run app.py
```
Buka http://localhost:8501

## Format Dataset
Wajib: product_id, product_name. Direkomendasikan: category, brand, description, price. Opsional: marketplace, rating, terjual, tanggal_upload.

## Test
```bash
python tests/test_recommender.py
```

Catatan: dataset bawaan adalah data simulasi menyerupai produk marketplace Indonesia.
