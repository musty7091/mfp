import streamlit as st
import pathlib
from auth import login_user, logout_user, check_login_status

# --- Sayfa ayarları ---
st.set_page_config(page_title="Modern Fatura Platformu", page_icon="🧾", layout="centered")

# --- Tema yükle ---
css_path = pathlib.Path(__file__).parent / "styles" / "mfp_theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# --- Oturum kontrolü ---
if check_login_status():
    # KUSURSUZ YÖNLENDİRME: Sadece dosya adı (pages/dashboard.py -> dashboard)
    st.switch_page("dashboard")

# --- Giriş sayfası arayüzü ---
st.markdown("<h1 style='text-align:center;'>🧾 Modern Fatura Platformu</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>İşletme içi teklif, sipariş ve faturalama arayüzü</p>", unsafe_allow_html=True)
st.divider()

st.subheader("🔒 Oturum Aç")

username = st.text_input("Kullanıcı Adı", placeholder="örn. admin")
password = st.text_input("Şifre", type="password")

if st.button("Giriş Yap"):
    token = login_user(username, password)
    if token:
        st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
        st.rerun()

# --- Footer ---
st.markdown("<p style='text-align:center; color:gray; font-size:13px; margin-top:2rem;'>© 2025 Modern Fatura Platformu · Via Solutions</p>", unsafe_allow_html=True)