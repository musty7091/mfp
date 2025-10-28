from pydantic import BaseModel, EmailStr

# Temel kullanıcı şeması
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False

# Kullanıcı oluşturma şeması (Şifre gerektirir)
class UserCreate(UserBase):
    password: str

# Kullanıcı okuma/dönüş şeması (Hassas verileri çıkarır)
class User(UserBase):
    id: int

    class Config:
        # SQLAlchemy ORM ile uyumluluk sağlar
        orm_mode = True