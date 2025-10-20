# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, RoleEnum
from app.core.security import get_current_user, admin_required
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

# ------------------- Schemas -------------------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.customer

# ------------------- Routes -------------------

@router.get("/", dependencies=[Depends(admin_required)])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "customer_id": u.customer_id,
        }
        for u in users
    ]

@router.get("/{user_id}", dependencies=[Depends(admin_required)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return user
