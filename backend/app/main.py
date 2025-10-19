# -*- coding: utf-8 -*-
"""
MFP (Mini Fatura Pro)
Ana Uygulama Dosyası
"""

from fastapi import FastAPI
from app.database import Base, engine
from app.models import product

# ------------------------------
# Veritabanı tablolarını oluştur
# ------------------------------
Base.metadata.create_all(bind=engine)

# ------------------------------
# FastAPI uygulaması
# ------------------------------
app = FastAPI(
    title="MFP",
    description="Mini Fatura Pro — Küçük işletmeler için fatura ve cari sistemi",
    version="0.1.0"
)

# ------------------------------
# Router'ları içe aktar
# ------------------------------
from app.routers import products
app.include_router(products.router)

# ------------------------------
# Ana test endpoint
# ------------------------------
@app.get("/")
def root():
    return {"message": "MFP sistemi çalışıyor 🚀"}
