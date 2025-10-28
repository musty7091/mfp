import streamlit as st
import pandas as pd
from auth import check_login_status, logout_user
from api_client import api_request
from session_token import get_auth_headers

# Streamlit sayfa yapılandırması
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# --- Oturum Kontrolü ve Yönlendirme ---
if not check_login_status():
    st.warning("Oturum sonlandı, lütfen tekrar giriş yapın.")
    # KUSURSUZ YÖNLENDİRME: Ana dosyaya geri dönüş (streamlit_app.py -> streamlit_app)
    st.switch_page("streamlit_app") 

st.title("📊 Yönetim Paneli (Dashboard)")

# --- Çıkış Butonu ---
if st.sidebar.button("Çıkış Yap"):
    logout_user()


@st.cache_data(ttl=60) 
def fetch_dashboard_data():
    """
    Backend API'sinden dashboard metriklerini ve son faturaları çeker.
    """
    
    headers = get_auth_headers()
    
    response = api_request(
        method="GET",
        endpoint="/dashboard/summary",
        headers=headers
    )

    if response and "error" not in response:
        return response
    
    st.error(f"Dashboard verileri çekilemedi. Hata: {response.get('error', 'API Bağlantısı Başarısız.')}")
    return None

# Verileri çek
dashboard_data = fetch_dashboard_data()

if dashboard_data:
    
    # --- Metrik Alanları (API'den Gelen Verilerle) ---
    metrics = dashboard_data.get("metrics", {})
    latest_invoices = dashboard_data.get("latest_invoices", [])
    
    ciro = metrics.get("monthly_revenue", 0.0)
    fatura_sayisi = metrics.get("total_invoices", 0)
    musteri_sayisi = metrics.get("active_customers", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Toplam Fatura Sayısı", fatura_sayisi)
    with col2:
        st.metric("Aylık Toplam Ciro", f"₺{ciro:,.2f}")
    with col3:
        st.metric("Aktif Müşteri", musteri_sayisi)

    st.divider()

    # --- Son Faturalar (API'den Gelen Verilerle) ---
    st.subheader("🧾 Son Faturalar")

    if latest_invoices:
        df = pd.DataFrame(latest_invoices)
        
        df['Tutar (₺)'] = df['amount'].apply(lambda x: f"₺{x:,.2f}")
        df = df.rename(columns={
            "invoice_number": "Fatura No",
            "customer_name": "Müşteri",
            "issue_date": "Tarih"
        })
        
        display_columns = ["Fatura No", "Müşteri", "Tarih", "Tutar (₺)"]
        
        st.dataframe(df[display_columns], use_container_width=True, hide_index=True)
    else:
        st.info("Gösterilecek son fatura kaydı bulunmamaktadır.")

# --- Footer ---
st.markdown("<p style='text-align:center; color:gray; font-size:13px; margin-top:2rem;'>© 2025 Modern Fatura Platformu · Via Solutions</p>", unsafe_allow_html=True)