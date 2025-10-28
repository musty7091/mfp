from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# Temel ürün alanları (Stok ve SKT takibi dahil)
class ProductBase(BaseModel):
    name: str = Field(..., description="Ürünün adı veya hizmetin tanımı.")
    unit_price: float = Field(..., gt=0, description="Ürünün birim satış fiyatı.")
    
    # Satılabilir ürün için kritik alanlar:
    stock_quantity: int = Field(0, ge=0, description="Mevcut stok miktarı.")
    sku: Optional[str] = Field(None, description="Stok Kodu (SKU).")
    expiration_date: Optional[date] = Field(None, description="Son kullanma tarihi (SKT).")


# Yeni ürün oluşturmak için kullanılan şema
class ProductCreate(ProductBase):
    # Oluşturma sırasında tüm temel alanlar gereklidir
    pass

# Ürün güncellemek için kullanılan şema (tüm alanlar isteğe bağlı olabilir)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    sku: Optional[str] = None
    expiration_date: Optional[date] = None

# Ürün verilerini okumak ve döndürmek için kullanılan şema
class Product(ProductBase):
    id: int # Veritabanı ID'si
    
    class Config:
        # Pydantic V2 uyumluluğu için 'from_attributes' kullanıyoruz
        from_attributes = True

# Projenin eski adlandırma beklentisine uyum için (ImportError'ı önler)
ProductResponse = Product