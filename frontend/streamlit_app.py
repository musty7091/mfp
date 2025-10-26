# --- GİRİŞ SAYFASI (Feather+Glass Tasarımı) ---
import streamlit as st
from pathlib import Path
from auth import login_user, is_authenticated, logout_user, get_token

# Sayfa ayarları
st.set_page_config(page_title="Modern Fatura Platformu", page_icon="🧾", layout="centered")

# CSS yükle
css_path = Path(__file__).parent / "styles" / "mfp_theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Oturum kontrolü
if is_authenticated():
    st.session_state["page"] = "dashboard"
    st.switch_page("pages/dashboard.py")

# --- Giriş Arayüzü ---
st.markdown("""
<div class="login-wrapper">
  <div class="login-card">
    <div class="login-header">
      <h1>🧾 Modern Fatura Platformu</h1>
      <p>İşletme içi teklif, sipariş ve faturalama arayüzü</p>
    </div>
    <div class="login-body">
      <h3>🔒 Oturum Aç</h3>
""", unsafe_allow_html=True)

# Form alanı
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("Kullanıcı Adı", placeholder="örn. admin")
    password = st.text_input("Şifre", type="password", placeholder="••••••••")
    submitted = st.form_submit_button("Giriş Yap")

    if submitted:
        token = login_user(username, password)
        if token:
            st.session_state["token"] = token
            st.session_state["page"] = "dashboard"
            st.success("✅ Oturum açıldı. Yönlendiriliyorsunuz...")
            st.rerun()
        else:
            st.error("❌ Kullanıcı adı veya şifre hatalı.")

st.markdown("""
    </div>
    <div class="login-footer">
      <p>© 2025 Modern Fatura Platformu · Via Solutions</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
