from fastapi import FastAPI
from app.database import Base, engine
from app.models import product, customer, invoice  # tüm modeller buradan çağrılır
from app.routers import products, customers
from app.routers import invoices



# ✅ Tüm tabloları oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MFP Backend", version="1.0")

# ✅ Router kayıtları
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(invoices.router)

@app.get("/")
def root():
    return {"message": "MFP sistemi çalışıyor 🚀"}
