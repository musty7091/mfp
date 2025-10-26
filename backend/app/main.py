from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import products

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MFP Backend API",
    version="1.0.0",
    description="Modern Fatura Platformu Backend Servisleri"
)

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router’lar
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "MFP Backend çalışıyor 🚀"}
