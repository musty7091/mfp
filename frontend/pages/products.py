import streamlit as st
import pandas as pd
from auth import is_authenticated

st.set_page_config(page_title="Ürünler", page_icon="📦", layout="wide")

if not is_authenticated():
    st.warning("Bu sayfayı görmek için giriş yapmalısınız.")
    st.stop()

st.title("📦 Ürün Yönetimi")

df = pd.DataFrame({
    "Ürün Adı": ["Rakı 70cl", "Viski 1L", "Şarap 75cl", "Vodka 1L", "Bira 50cl"],
    "Stok": [34, 20, 56, 12, 87],
    "Fiyat (₺)": [650, 1120, 240, 580, 65]
})

st.dataframe(df, use_container_width=True)
st.divider()

st.subheader("Yeni Ürün Ekle")
with st.form("urun_ekle"):
    urun = st.text_input("Ürün Adı")
    stok = st.number_input("Stok Miktarı", min_value=0)
    fiyat = st.number_input("Birim Fiyat (₺)", min_value=0.0)
    ekle = st.form_submit_button("Kaydet")

    if ekle:
        if urun:
            st.success(f"✅ {urun} başarıyla eklendi (demo mod).")
        else:
            st.warning("Ürün adı boş bırakılamaz.")
