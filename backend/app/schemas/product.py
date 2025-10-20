from pydantic import BaseModel
from enum import Enum
from typing import Optional

class VatRateEnum(float, Enum):
    zero = 0.0
    low = 5.0
    medium = 10.0
    reduced = 16.0
    standard = 20.0
    special = -1.0

class ProductBase(BaseModel):
    name: str
    barcode: Optional[str] = None
    unit_price: float
    vat_rate: VatRateEnum = VatRateEnum.standard

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
