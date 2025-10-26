# ------------------------------------------------------------
# Modern Fatura Platformu — Auth Yönetimi
# ------------------------------------------------------------
# Kullanıcı oturumunu Streamlit session_state üzerinde yönetir.
# ------------------------------------------------------------

import streamlit as st

# Oturum kontrolü
def is_authenticated() -> bool:
    """Kullanıcının giriş yapıp yapmadığını döner."""
    return "token" in st.session_state and st.session_state["token"] is not None

def login_user(token: str):
    """Kullanıcıyı oturum açmış olarak işaretler."""
    st.session_state["token"] = token

def logout_user():
    """Kullanıcının oturumunu kapatır."""
    if "token" in st.session_state:
        del st.session_state["token"]

def get_token() -> str:
    """Aktif oturumdaki kullanıcı token’ını döner."""
    return st.session_state.get("token")
