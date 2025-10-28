from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base
import enum

# Kullanıcı Rollerini tanımlayan Enum
class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    READ_ONLY = "READ_ONLY"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # YENİ: RoleEnum'u veritabanına ekliyoruz
    role = Column(Enum(RoleEnum), default=RoleEnum.EMPLOYEE, nullable=False)