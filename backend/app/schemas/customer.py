from pydantic import BaseModel
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    tax_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    default_discount: float = 0.0

class CustomerResponse(BaseModel):
    id: int
    name: str
    tax_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    default_discount: float

    class Config:
        from_attributes = True
