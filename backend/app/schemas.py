from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    barcode: Optional[str] = None
    name: str
    unit: Optional[str] = "Adet"
    price: float
    vat: float = 0.0

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True
class CustomerCreate(BaseModel):
    name: str
    tax_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    default_discount: float = 0.0

class CustomerResponse(CustomerCreate):
    id: int
    class Config:
        from_attributes = True  # orm_mode yerine (Pydantic v2 için)
from datetime import datetime

class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: float
    discount_rate: float = 0.0


class InvoiceCreate(BaseModel):
    customer_id: int
    items: list[InvoiceItemCreate]


class InvoiceResponse(BaseModel):
    id: int
    date: datetime
    customer_id: int
    subtotal: float
    vat_total: float
    discount_total: float
    grand_total: float

    class Config:
        from_attributes = True
