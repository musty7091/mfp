# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, users, customers, products, invoices

# -------------------- Veritabanı Başlat --------------------
Base.metadata.create_all(bind=engine)

# -------------------- Uygulama Nesnesi --------------------
app = FastAPI(
    title="MFP Backend API",
    description="Modern Fatura Platformu - Backend Servisleri",
    version="1.0.0",
    contact={
        "name": "MFP Developer Team",
        "email": "dev@mfp.com",
    },
)

# -------------------- CORS Ayarları --------------------
origins = [
    "http://localhost:3000",   # React / Vue / Streamlit frontend
    "http://127.0.0.1:3000",
    "http://localhost:8501",   # Streamlit
    "http://127.0.0.1:8501",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Router’ların Dahil Edilmesi --------------------
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(invoices.router)

# -------------------- Kök Endpoint --------------------
@app.get("/")
def root():
    return {
        "message": "🚀 MFP Backend aktif!",
        "status": "OK",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# -------------------- Geliştirici Notu --------------------
"""
Kullanım:
    uvicorn app.main:app --reload

Örnek API’ler:
    POST   /auth/register
    POST   /auth/login
    GET    /users
    GET    /customers
    POST   /invoices/create
"""
