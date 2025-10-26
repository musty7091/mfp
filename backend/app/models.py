from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    vat_rate = Column(Float, nullable=False, default=0.20)
    stock = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
