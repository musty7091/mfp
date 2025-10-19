from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    customer = "customer"
    representative = "representative"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.customer)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    # Customer ile birebir ilişki
    customer = relationship("Customer", back_populates="user", lazy="joined")
