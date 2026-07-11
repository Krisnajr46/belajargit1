"""Pemuatan & normalisasi dataset (cache Streamlit)."""
import pandas as pd
import streamlit as st
from config import DATA_PATH, ID_COL, NAME_COL, OPTIONAL_COLUMNS
from src.preprocessing import build_content


@st.cache_data(show_spinner="Memuat dataset produk...")
def load_products(path=DATA_PATH):
    return _prepare(pd.read_csv(path))


@st.cache_data(show_spinner=False)
def load_uploaded_products(file):
    return _prepare(pd.read_csv(file))


def _prepare(df):
    _validate(df)
    df = df.drop_duplicates(subset=[ID_COL]).reset_index(drop=True)
    df = _fill_optional(df)
    return build_content(df)


def _validate(df):
    for required in (ID_COL, NAME_COL):
        if required not in df.columns:
            raise ValueError("Kolom wajib '" + required + "' tidak ditemukan.")


def _fill_optional(df):
    df = df.copy()
    for col, default in OPTIONAL_COLUMNS.items():
        if col not in df.columns:
            df[col] = default
    return df
