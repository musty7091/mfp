from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from app.database import get_db
from app.models import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


# --- Tüm Ürünler ---
@router.get("/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id.desc()).all()


# --- Tekil Ürün ---
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
    return product


# --- Yeni Ürün ---
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.barcode == product.barcode).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu barkoda sahip ürün zaten mevcut.")
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# --- Güncelleme ---
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated_data: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


# --- Silme ---
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
    db.delete(db_product)
    db.commit()
    return {"detail": "Ürün başarıyla silindi."}


# --- SKT Yaklaşanlar ---
@router.get("/expiry/soon", response_model=List[ProductResponse])
def products_expiring_soon(days: int = 30, db: Session = Depends(get_db)):
    today = date.today()
    limit_date = today + timedelta(days=days)
    products = (
        db.query(Product)
        .filter(Product.expiry_date != None)
        .filter(Product.expiry_date <= limit_date)
        .order_by(Product.expiry_date.asc())
        .all()
    )
    return products
