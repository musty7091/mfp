import streamlit as st
import requests
import json
import os

BACKEND_URL = "http://localhost:8000"
TOKEN_FILE = "session_token.json"


# --- Yardımcı fonksiyonlar ---
def save_token(token_data):
    """Token bilgisini JSON dosyasına kaydeder."""
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)


def load_token():
    """Kayıtlı token varsa geri döndürür."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def delete_token():
    """Token dosyasını siler (çıkış yapma işlemi)."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


# --- Login / Logout işlemleri ---
def login_user(username, password):
    """Kullanıcı girişini backend üzerinden doğrular."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            data={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            save_token({"token": token, "username": username})
            st.session_state["token"] = token
            st.session_state["username"] = username
            st.session_state["is_authenticated"] = True
            return token
        else:
            st.error("Giriş başarısız. Bilgileri kontrol edin.")
            return None
    except Exception as e:
        st.error(f"Sunucuya bağlanılamadı: {e}")
        return None


def logout_user():
    """Kullanıcıyı sistemden çıkartır."""
    delete_token()
    st.session_state.clear()
    st.rerun()


def check_login_status():
    """Kullanıcı giriş yapmış mı kontrol eder."""
    token_data = load_token()
    if token_data and "token" in token_data:
        st.session_state["is_authenticated"] = True
        st.session_state["token"] = token_data["token"]
        st.session_state["username"] = token_data["username"]
        return True
    return False
