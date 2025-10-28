from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.core.security import get_current_user, rep_required

router = APIRouter(prefix="/products", tags=["Products"])

# Simülasyon: Ürün verilerini stok ve SKT bilgileriyle tutuyoruz.
DUMMY_PRODUCTS = [
    Product(id=1, name="Yazılım Geliştirme Hizmeti", unit_price=500.0, stock_quantity=9999, sku="HIZ-SW", expiration_date=None, barcode="0001", vat_rate=20.0),
    Product(id=2, name="A4 Ofis Kağıdı (Koli)", unit_price=120.0, stock_quantity=45, sku="STK-001", expiration_date=date(2026, 12, 31), barcode="0002", vat_rate=20.0),
    Product(id=3, name="Özel Tasarım Lisansı", unit_price=1500.0, stock_quantity=1, sku="HIZ-LIS", expiration_date=None, barcode="0003", vat_rate=20.0),
]
product_id_counter = 4

@router.get("/", response_model=list[Product])
def read_products(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """Tüm ürünleri stok ve SKT bilgileriyle listeler (Yetkili kullanıcı gerektirir)."""
    # Gerçek uygulamada DB sorgusu burada olur.
    return DUMMY_PRODUCTS

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(rep_required)])
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """Yeni ürün/stok kaydı oluşturur (Temsilci/Admin yetkisi gerektirir)."""
    global product_id_counter
    
    # Yeni ürün verisini simülasyon listesine ekle
    new_product_dict = product.dict()
    new_product_dict["id"] = product_id_counter
    
    # Varsayılan KDV ve barkodu ekliyoruz (Model ile uyumlu olması için)
    new_product_dict["barcode"] = f"AUTO-{product_id_counter}" 
    new_product_dict["vat_rate"] = new_product_dict.get("vat_rate", 20.0) 

    new_product = Product(**new_product_dict)
    DUMMY_PRODUCTS.append(new_product)
    product_id_counter += 1
    
    return new_product