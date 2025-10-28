from datetime import datetime, timedelta
from typing import Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from functools import wraps 
from app.models.user import RoleEnum # RoleEnum'u kullanıyoruz

# Projeniz için gizli anahtar ve algoritma
SECRET_KEY = "EN_GUCLU_GIZLI_ANAHTAR_BURAYA_GELMELI_2025" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 1 hafta geçerli

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") 

# --- Şifre İşlemleri ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Düz metin şifreyi hashlenmiş şifre ile karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Verilen şifreyi hashler."""
    return pwd_context.hash(password)

# --- JWT Token İşlemleri ---

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """JWT Erişim Jetonu (Access Token) oluşturur."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # "sub" (subject) claim'i ve rol bilgisini token içine ekliyoruz
    to_encode.update({"exp": expire, "sub": to_encode.get("username"), "role": to_encode.get("role")}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Kullanıcı Doğrulama (Simülasyon) ---

def get_user_by_username(db: Session, username: str):
    """Kullanıcıyı veritabanında kullanıcı adına göre bulur (Simülasyon)."""
    # Varsayılan şifre: 123456
    if username == "admin":
        return {
            "id": 1,
            "username": "admin",
            "email": "admin@mfp.com",
            "hashed_password": get_password_hash("123456"), 
            "is_active": True,
            "is_admin": True,
            "role": RoleEnum.ADMIN.value 
        }
    return None

def authenticate_user(db: Session, username: str, password: str):
    """Kullanıcı adı ve şifre ile kullanıcıyı doğrular."""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# --- Yetkilendirme Kontrolü ---

def get_current_user(token: str = Depends(oauth2_scheme)): 
    """JWT token'dan mevcut kullanıcıyı çıkarır ve döndürür."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik bilgileri doğrulanamadı",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_role: str = payload.get("role") 
        if username is None or user_role is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    return {"username": username, "role": user_role}

# YENİ EKLENTİ: Rol Kontrol Mekanizması
def role_required(allowed_roles: list[RoleEnum]):
    """Belirtilen rollerden birine sahip kullanıcı gerektiren bağımlılık."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in [r.value for r in allowed_roles]:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Erişim reddedildi. Bu işlem için {', '.join([r.name for r in allowed_roles])} yetkisi gereklidir."
            )
        return current_user
    return role_checker

# rep_required (Temsilci gereklidir)
# Fatura kesme, ürün/müşteri ekleme gibi işlemler için genelde ADMIN, MANAGER ve EMPLOYEE yetkileri istenir.
rep_required = role_required([RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.EMPLOYEE])

# admin_required (Admin gereklidir)
# Kullanıcı yönetimi, sistem ayarları gibi kritik işlemler için sadece ADMIN yetkisi istenir.
admin_required = role_required([RoleEnum.ADMIN])