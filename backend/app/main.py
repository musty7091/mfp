from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import products, customers, invoices, users, auth, dashboard # Yeni router'lar dahil edildi

# Veritabanı tablolarını oluştur
# Bu satır, uygulama başlamadan önce tüm modellerin tablolarını oluşturur.
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

# Router’ları Dahil Etme
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(invoices.router, prefix="/api/v1/invoices", tags=["Invoices"])


@app.get("/")
def root():
    return {"message": "MFP Backend çalışıyor 🚀"}