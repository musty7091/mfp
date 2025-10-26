from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# --- Ortak Alanlar ---
class ProductBase(BaseModel):
    name: str
    barcode: str
    price: float
    vat_rate: float
    stock: int
    expiry_date: Optional[date] = None


# --- Yeni Ürün ---
class ProductCreate(ProductBase):
    pass


# --- Ürün Güncelleme ---
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    price: Optional[float] = None
    vat_rate: Optional[float] = None
    stock: Optional[int] = None
    expiry_date: Optional[date] = None


# --- Yanıt Modeli ---
class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 için
