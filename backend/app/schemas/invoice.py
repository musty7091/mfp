from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: float
    discount_rate: float = 0.0


class InvoiceCreate(BaseModel):
    customer_id: int
    items: List[InvoiceItemCreate]


class InvoiceItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: float
    unit_price: float
    discount_rate: float
    vat_rate: float
    line_total: float

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: int
    date: datetime
    customer_id: int
    subtotal: float
    vat_total: float
    discount_total: float
    grand_total: float
    items: List[InvoiceItemResponse]

    class Config:
        from_attributes = True
