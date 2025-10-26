import streamlit as st
import pandas as pd
from auth import is_authenticated, get_token

st.set_page_config(page_title="Müşteriler", page_icon="👥", layout="wide")

if not is_authenticated():
    st.warning("Bu sayfayı görmek için giriş yapmalısınız.")
    st.stop()

st.title("👥 Müşteri Yönetimi")

# --- Dummy müşteri listesi (ileride API'den çekilecek) ---
data = pd.DataFrame({
    "Müşteri Adı": ["Ali Market", "Beyza Ltd.", "Deniz Gıda", "Elite Cafe", "Fırat Tekstil"],
    "Telefon": ["0543 200 12 12", "0532 541 00 11", "0392 228 44 55", "0542 999 88 77", "0533 444 22 11"],
    "Adres": ["Lefkoşa", "Girne", "Gazimağusa", "Güzelyurt", "İskele"]
})

arama = st.text_input("Müşteri Ara", placeholder="İsim veya telefon girin...")
if arama:
    data = data[data["Müşteri Adı"].str.contains(arama, case=False, na=False)]

st.dataframe(data, use_container_width=True)

st.divider()
st.subheader("➕ Yeni Müşteri Ekle")

with st.form("yeni_musteri_formu"):
    ad = st.text_input("Müşteri Adı")
    tel = st.text_input("Telefon")
    adres = st.text_area("Adres")
    kaydet = st.form_submit_button("Kaydet")

    if kaydet:
        if ad and tel:
            st.success(f"✅ '{ad}' başarıyla eklendi (demo mod).")
        else:
            st.warning("Lütfen müşteri adı ve telefon alanlarını doldurun.")
