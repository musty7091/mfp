from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    barcode: Optional[str] = None
    price: float
    vat: float

class ProductResponse(BaseModel):
    id: int
    name: str
    barcode: Optional[str] = None
    price: float
    vat: float

    class Config:
        from_attributes = True
