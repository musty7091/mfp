# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product, VatRateEnum
from app.models.user import User, RoleEnum
from app.core.security import get_current_user, rep_required
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["Products"])

class ProductCreate(BaseModel):
    name: str
    barcode: str | None = None
    price: float
    vat_rate: VatRateEnum = VatRateEnum.standard

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post("/", dependencies=[Depends(rep_required)])
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.name == product_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu ürün zaten mevcut.")
    product = Product(
        name=product_data.name,
        barcode=product_data.barcode,
        unit_price=product_data.price,
        vat_rate=product_data.vat_rate
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", dependencies=[Depends(rep_required)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
    db.delete(product)
    db.commit()
    return {"message": "Ürün silindi."}
