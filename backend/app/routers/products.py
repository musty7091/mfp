from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product

router = APIRouter(prefix="/products", tags=["Products"])

# DB bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
