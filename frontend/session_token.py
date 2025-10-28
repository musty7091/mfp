import streamlit as st

def get_auth_headers():
    """Streamlit oturumundan JWT yetkilendirme başlıklarını döndürür."""
    token = st.session_state.get('access_token')
    token_type = st.session_state.get('token_type', 'Bearer')
    
    if token:
        # API isteği için gereken Authorization başlığını döndürür.
        return {
            "Authorization": f"{token_type} {token}"
        }
    return {}