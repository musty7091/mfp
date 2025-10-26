from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductBase(BaseModel):
    ad: str
    barkod: str
    birim_fiyat: float
    kdv_orani: float
    stok_miktari: int
    skt: Optional[date] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    ad: Optional[str]
    barkod: Optional[str]
    birim_fiyat: Optional[float]
    kdv_orani: Optional[float]
    stok_miktari: Optional[int]
    skt: Optional[date]

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
