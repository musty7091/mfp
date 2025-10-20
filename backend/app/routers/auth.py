# -*- coding: utf-8 -*-
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, RoleEnum
from app.models.customer import Customer
from app.core.security import (
    create_access_token,
    get_password_hash,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ---------------------- Şema Tanımları ----------------------

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.customer
    customer_id: int | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------------------- Kullanıcı Kayıt ----------------------

@router.post("/register", response_model=TokenResponse)
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("customer"),
    customer_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    """
    Yeni kullanıcı oluşturur. Varsayılan rol "customer"dır.
    """
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı zaten mevcut.")

    # Eğer müşteri hesabıysa, customer_id kontrolü
    if role == RoleEnum.customer and not customer_id:
        raise HTTPException(
            status_code=400,
            detail="Customer rolü için 'customer_id' alanı gereklidir."
        )

    hashed_pw = get_password_hash(password)
    user = User(
        username=username,
        email=email,
        password_hash=hashed_pw,
        role=role,
        customer_id=customer_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": token, "token_type": "bearer"}

# ---------------------- Giriş (Login) ----------------------

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Kullanıcı girişi yapar ve JWT token döner.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

# ---------------------- Kullanıcı Bilgisi ----------------------

from app.core.security import get_current_user  # dosyanın en üstüne ekle

@router.get("/me", response_model=None)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Aktif kullanıcının bilgilerini döner.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "customer_id": current_user.customer_id,
    }