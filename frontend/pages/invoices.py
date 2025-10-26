import streamlit as st
import pandas as pd
from auth import check_login_status, logout_user

st.set_page_config(page_title="Müşteriler", page_icon="👥", layout="wide")

# Oturum kontrolü
if not check_login_status():
    st.warning("🔒 Oturum süresi doldu veya çıkış yaptınız.")
    st.switch_page("streamlit_app.py")
    st.stop()

st.title("💰 Fatura Yönetimi")

faturalar = pd.DataFrame({
    "Fatura No": ["INV-001", "INV-002", "INV-003"],
    "Müşteri": ["Ali Market", "Deniz Gıda", "Elite Cafe"],
    "Tarih": ["2025-10-24", "2025-10-25", "2025-10-26"],
    "Tutar (₺)": [1950.5, 4875.75, 1230.90]
})

st.dataframe(faturalar, use_container_width=True)

st.divider()
st.subheader("Yeni Fatura Oluştur")

with st.form("fatura_formu"):
    musteri = st.text_input("Müşteri Adı")
    tarih = st.date_input("Fatura Tarihi")
    tutar = st.number_input("Fatura Tutarı (₺)", min_value=0.0)
    kaydet = st.form_submit_button("Kaydet")

    if kaydet:
        if musteri and tutar > 0:
            st.success(f"✅ Fatura başarıyla kaydedildi (demo mod).")
        else:
            st.warning("Lütfen müşteri ve tutar bilgilerini girin.")
