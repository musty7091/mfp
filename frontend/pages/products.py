import streamlit as st
import pandas as pd
from datetime import date
from auth import check_login_status
from api_client import api_request
from session_token import get_auth_headers

# Sayfa Ayarları
st.set_page_config(page_title="Ürünler ve Stok", page_icon="📦", layout="wide")

# --- Oturum Kontrolü ---
if not check_login_status():
    st.warning("Erişim reddedildi. Lütfen tekrar giriş yapın.")
    # Kritik Düzeltme: Ana sayfaya uzantısız yönlendirme
    st.switch_page("streamlit_app")

st.title("📦 Ürün ve Stok Yönetimi")
st.markdown("İşletmenizin ürün/hizmet, stok ve SKT (Son Kullanma Tarihi) bilgilerini yönetin.")

# --- API İsteği Fonksiyonu ---
@st.cache_data(ttl=60) # Ürün listesini 1 dakika önbellekte tut
def fetch_products():
    """Backend'den tüm ürün verilerini çeker (Stok ve SKT dahil)."""
    headers = get_auth_headers()
    
    response = api_request(
        method="GET",
        endpoint="/products",
        headers=headers
    )
    
    if response and "error" not in response:
        return response
    
    st.error(f"Ürün verileri çekilemedi: {response.get('error', 'Bilinmeyen Hata')}")
    return []

# --- Ürün Listesini Göster ---
product_data = fetch_products()

if product_data:
    df = pd.DataFrame(product_data)
    
    # Tarih formatını düzenleme (SKT için)
    df['expiration_date'] = pd.to_datetime(df['expiration_date']).dt.strftime('%Y-%m-%d').replace('NaT', '-')
    
    # Sütunları Türkçeleştirme
    df = df.rename(columns={
        "name": "Ürün Adı",
        "unit_price": "Birim Fiyat (₺)",
        "stock_quantity": "Stok Miktarı",
        "sku": "SKU (Stok Kodu)",
        "expiration_date": "Son Kullanma Tarihi (SKT)"
    })
    
    # Fiyat ve Stok formatlaması
    df["Birim Fiyat (₺)"] = df["Birim Fiyat (₺)"].apply(lambda x: f"₺{x:,.2f}")
    
    display_columns = ["Ürün Adı", "SKU (Stok Kodu)", "Birim Fiyat (₺)", "Stok Miktarı", "Son Kullanma Tarihi (SKT)"]
    
    st.dataframe(df[display_columns], use_container_width=True, hide_index=True)
else:
    st.info("Kayıtlı ürün bulunmamaktadır.")

st.divider()

# --- Yeni Ürün Ekleme Formu (Stok/SKT Dahil) ---
with st.expander("📦 Yeni Ürün/Stok Ekle", expanded=False):
    with st.form("new_product_form"):
        col_form_1, col_form_2 = st.columns(2)
        with col_form_1:
            new_name = st.text_input("Ürün Adı *")
            new_price = st.number_input("Birim Fiyatı (₺) *", min_value=0.01, format="%.2f")
            new_sku = st.text_input("SKU (Stok Kodu)")
        with col_form_2:
            new_stock = st.number_input("Stok Miktarı", min_value=0, step=1)
            new_expiry_date = st.date_input("Son Kullanma Tarihi (SKT)", value=None, min_value=date.today())
            
        submitted = st.form_submit_button("Ürünü Kaydet")
        
        if submitted:
            if not new_name or not new_price:
                st.error("Lütfen Ürün Adını ve Birim Fiyatını girin.")
            else:
                product_data = {
                    "name": new_name,
                    "unit_price": new_price,
                    "stock_quantity": new_stock,
                    "sku": new_sku,
                    "expiration_date": new_expiry_date.isoformat() if new_expiry_date else None
                }
                
                headers = get_auth_headers()
                response = api_request(
                    method="POST",
                    endpoint="/products",
                    data=product_data,
                    headers=headers
                )
                
                if "error" not in response:
                    st.success(f"'{new_name}' başarıyla kaydedildi (ID: {response.get('id')})!")
                    st.cache_data.clear()
                    st.rerun() 
                else:
                    st.error(f"Kaydetme hatası: {response.get('error', 'Bilinmeyen API Hatası')}")