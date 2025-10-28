# main.py

import subprocess
import sys

# Ana Streamlit uygulamasının dosya adını tanımla
# Streamlit'in eski sürümü "main.py" olarak çalıştığında, 
# diğer sayfaları çalıştırmak için "streamlit run" komutunu kullanmak en güvenli yoldur.

# Bu betiğin Streamlit tarafından çalıştırıldığını varsayıyoruz.
# Eğer bu betiği bir terminalden doğrudan çalıştırmak isterseniz (önerilen yol):
# streamlit run streamlit_app.py

# Alternatif ve daha temiz çözüm: streamlit_app.py içeriğini buraya alalım
# Ancak bu, modüler yapınızı bozar.
# En iyisi, main.py'yi tamamen atlayıp Streamlit'i doğrudan streamlit_app.py ile başlatmaktır.

# Müşteri olarak size en basit ve güvenilir nihai kodu vermek için, 
# main.py'deki yönlendirme satırını kaldırıp, 
# tüm uygulamanın tek bir Streamlit ana dosyası üzerinden çalıştırılmasını sağlamalıyız.

# Nihai Kural: Streamlit uygulaması "streamlit run streamlit_app.py" komutu ile başlatılmalıdır.

# Eğer Streamlit uygulaması bir klasör yapısında başlatılıyorsa, 
# st.switch_page("streamlit_app.py") yerine tam dosya adını kullanmanız gerekir.

# Yönlendirme sorununu gidermek için, basitçe bu dosyayı temizleyip 
# Streamlit'i doğrudan ana dosyanızla başlatmanızı öneriyorum.

# Lütfen bu dosyayı **tamamen silin** ve uygulamanızı terminalden 
# aşağıdaki komutla başlatın (Eğer Streamlit'in yeni sayfa yapısını kullanmıyorsanız):

# Terminalde: streamlit run streamlit_app.py

# VEYA, Eğer main.py'yi tutmak zorundaysanız ve streamlit_app.py aynı dizindeyse:
import streamlit as st

# st.switch_page("streamlit_app.py") yerine, streamlit_app'i doğrudan çalıştıralım.
try:
    with open("streamlit_app.py", "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, st.__dict__)
except FileNotFoundError:
    st.error("Ana uygulama dosyası (streamlit_app.py) bulunamadı.")
except Exception as e:
    st.error(f"Ana uygulama yüklenirken bir hata oluştu: {e}")