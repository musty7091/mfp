from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten mevcut")
    hashed = get_password_hash(password)
    user = User(username=username, email=email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Kullanıcı oluşturuldu", "user_id": user.id}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
