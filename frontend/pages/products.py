import streamlit as st
import requests
from datetime import date

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Ürün Yönetimi", page_icon="📦", layout="wide")

st.title("📦 Ürün Yönetimi")
st.markdown("Kayıtlı ürünlerinizi yönetin veya yeni ürün ekleyin.")

# --- Oturum kontrolü ---
if "token" not in st.session_state:
    st.error("Bu sayfayı görmek için giriş yapmalısınız.")
    st.stop()

# --- Yardımcı fonksiyonlar ---
def get_products():
    res = requests.get(f"{BACKEND_URL}/products/")
    if res.status_code == 200:
        return res.json()
    else:
        st.error("Ürünler yüklenemedi.")
        return []

def add_product(data):
    res = requests.post(f"{BACKEND_URL}/products/", json=data)
    if res.status_code == 201:
        st.success("✅ Ürün başarıyla eklendi.")
        st.rerun()
    else:
        st.error(f"❌ Ürün eklenemedi: {res.text}")

# --- Ana sayfa görünümü ---
products = get_products()

if "show_form" not in st.session_state:
    st.session_state.show_form = False

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.subheader("📋 Kayıtlı Ürünler")
with col2:
    if st.button("➕ Ürün Ekle", use_container_width=True):
        st.session_state.show_form = not st.session_state.show_form

# --- Ürün tablosu ---
if products:
    st.dataframe(
        [
            {
                "Barkod": p["barkod"],
                "Ürün Adı": p["ad"],
                "Stok": p["stok_miktari"],
                "SKT": p["skt"] or "-",
            }
            for p in products
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Kayıtlı ürün bulunamadı.")

# --- Ürün ekleme formu ---
if st.session_state.show_form:
    st.markdown("---")
    st.subheader("🆕 Yeni Ürün Ekle")

    with st.form("product_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad = st.text_input("Ürün Adı", placeholder="ör. Jack Daniels 70cl")
            barkod = st.text_input("Barkod", placeholder="ör. 8691234567890")
            fiyat = st.number_input("Fiyat (₺)", min_value=0.0, step=0.5)
        with col2:
            kdv = st.number_input("KDV", min_value=0.0, max_value=1.0, step=0.01, value=0.2)
            stok = st.number_input("Stok", min_value=0, step=1, value=0)
            skt = st.date_input("SKT", value=None, min_value=date.today())

        submitted = st.form_submit_button("💾 Kaydet", use_container_width=True)
        if submitted:
            if not ad or not barkod:
                st.warning("Lütfen tüm zorunlu alanları doldurun.")
            else:
                data = {
                    "ad": ad,
                    "barkod": barkod,
                    "birim_fiyat": fiyat,
                    "kdv_orani": kdv,
                    "stok_miktari": stok,
                    "skt": str(skt) if skt else None,
                }
                add_product(data)
