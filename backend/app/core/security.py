# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, RoleEnum

# ------------------ JWT / Şifreleme Ayarları ------------------

SECRET_KEY = "super-secret-key-change-this"  # ⛔ Gerçek projede ENV’den okunmalı!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 saat oturum süresi

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ------------------ Şifre İşlemleri ------------------

def verify_password(plain_password, hashed_password):
    """Girilen parolayı hash ile karşılaştırır"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """Parolayı hash’ler"""
    # Bcrypt 72 byte sınırı
    password = password[:72]
    return pwd_context.hash(password)

# ------------------ JWT Token Üretimi ------------------

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """JWT access token oluşturur"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ------------------ Kullanıcı Doğrulama ------------------

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Token’dan aktif kullanıcıyı döner"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# ------------------ Rol Kontrol Fonksiyonları ------------------

def admin_required(current_user: User = Depends(get_current_user)):
    """Sadece Admin erişimi"""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Bu işlem için admin yetkisi gerekli.")
    return current_user

def rep_required(current_user: User = Depends(get_current_user)):
    """Admin veya Temsilci erişimi"""
    if current_user.role not in [RoleEnum.admin, RoleEnum.representative]:
        raise HTTPException(status_code=403, detail="Bu işlem için temsilci veya admin yetkisi gerekli.")
    return current_user

def customer_required(current_user: User = Depends(get_current_user)):
    """Sadece müşteri erişimi"""
    if current_user.role != RoleEnum.customer:
        raise HTTPException(status_code=403, detail="Bu işlem yalnızca müşterilere açıktır.")
    return current_user

def viewer_or_higher(current_user: User = Depends(get_current_user)):
    """Viewer, Representative, Admin erişimi"""
    if current_user.role not in [RoleEnum.viewer, RoleEnum.representative, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Bu işlem yalnızca izleyici ve üzeri roller içindir.")
    return current_user

# ------------------ Yardımcı: Token Üretim Yardımcısı ------------------

def authenticate_user(db: Session, username: str, password: str):
    """Kullanıcı adı ve parolayı doğrular"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
