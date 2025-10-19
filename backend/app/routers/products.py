from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product
from app.schemas import ProductCreate, ProductResponse

# ✅ Router tanımı burada olmalı (en üstte)
router = APIRouter(prefix="/products", tags=["Products"])

# ✅ DB bağlantı fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Ürün listeleme
@router.get("/")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# ✅ Ürün ekleme
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.barcode == product.barcode).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu barkod zaten kayıtlı.")
    
    new_product = Product(
        barcode=product.barcode,
        name=product.name,
        unit=product.unit,
        price=product.price,
        vat=product.vat
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
# ✅ Ürün Güncelleme
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")

    product.barcode = updated.barcode
    product.name = updated.name
    product.unit = updated.unit
    product.price = updated.price
    product.vat = updated.vat

    db.commit()
    db.refresh(product)
    return product


# ✅ Ürün Silme
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
    
    db.delete(product)
    db.commit()
    return {"message": f"{product.name} başarıyla silindi."}
