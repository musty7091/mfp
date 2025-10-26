import streamlit as st
import pandas as pd
from auth import is_authenticated

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if not is_authenticated():
    st.warning("Bu sayfayı görüntülemek için önce giriş yapmalısınız.")
    st.stop()

st.title("📊 Dashboard")

# --- Dummy veriler (ileride backend'e bağlanacak) ---
ciro = 482000.75
fatura_sayisi = 128
musteri_sayisi = 43

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Toplam Fatura Sayısı", fatura_sayisi)
with col2:
    st.metric("Aylık Toplam Ciro", f"₺{ciro:,.2f}")
with col3:
    st.metric("Aktif Müşteri", musteri_sayisi)

st.divider()

st.subheader("🧾 Son Faturalar")

df = pd.DataFrame({
    "Fatura No": ["INV-001", "INV-002", "INV-003", "INV-004", "INV-005"],
    "Müşteri": ["Ali Market", "Beyza Ltd.", "Deniz Gıda", "Elite Cafe", "Fırat Tekstil"],
    "Tarih": ["2025-10-21", "2025-10-22", "2025-10-23", "2025-10-24", "2025-10-25"],
    "Tutar (₺)": [1950.50, 2320.00, 4875.75, 1230.90, 3410.25]
})

st.dataframe(df, use_container_width=True)
