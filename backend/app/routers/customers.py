# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.models.user import User, RoleEnum
from app.core.security import get_current_user, rep_required
from pydantic import BaseModel

router = APIRouter(prefix="/customers", tags=["Customers"])

# ------------------- Schemas -------------------

class CustomerCreate(BaseModel):
    name: str
    tax_number: str | None = None
    address: str | None = None
    phone: str | None = None
    default_discount: float | None = 0.0

# ------------------- Routes -------------------

@router.get("/")
def list_customers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Admin ve temsilciler tüm müşterileri görebilir, müşteriler sadece kendi kayıtlarını görür"""
    if current_user.role == RoleEnum.customer:
        if not current_user.customer_id:
            raise HTTPException(status_code=404, detail="Müşteri kaydı bulunamadı.")
        return db.query(Customer).filter(Customer.id == current_user.customer_id).first()

    return db.query(Customer).all()

@router.post("/", dependencies=[Depends(rep_required)])
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = Customer(
        name=customer_data.name,
        tax_number=customer_data.tax_number,
        address=customer_data.address,
        phone=customer_data.phone,
        default_discount=customer_data.default_discount,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.delete("/{customer_id}", dependencies=[Depends(rep_required)])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı.")
    db.delete(customer)
    db.commit()
    return {"message": "Müşteri başarıyla silindi."}
