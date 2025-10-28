import streamlit as st
from api_client import api_request

def login_user(username: str, password: str):
    """
    Kullanıcıyı FastAPI backend'i üzerinden login eder ve token'ı Streamlit oturumunda saklar.
    """
    
    login_data = {
        "username": username,
        "password": password
    }
    
    # Login isteğini Form verisi (is_form_data=True) olarak gönderiyoruz.
    response = api_request(
        method="POST", 
        endpoint="/auth/login", 
        data=login_data,
        is_form_data=True # Login endpoint'i için Form verisi gönder
    )
    
    if "access_token" in response:
        # Token'ı Streamlit oturum durumunda (session state) sakla
        st.session_state['logged_in'] = True
        st.session_state['access_token'] = response["access_token"]
        st.session_state['token_type'] = response.get("token_type", "bearer")
        return response["access_token"]
    else:
        st.error(response.get("error", "Giriş başarısız oldu. Lütfen bilgilerinizi kontrol edin."))
        return None

def logout_user():
    """Oturum durumunu sıfırlar ve kullanıcıyı çıkış yapar."""
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']
    if 'access_token' in st.session_state:
        del st.session_state['access_token']
    if 'token_type' in st.session_state:
        del st.session_state['token_type']
    st.info("Başarıyla çıkış yaptınız. Yeniden yönlendiriliyorsunuz...")
    st.rerun() # Çıkış sonrası yenileme

def check_login_status() -> bool:
    """Kullanıcının şu anda oturum açıp açmadığını kontrol eder."""
    return st.session_state.get('logged_in', False)