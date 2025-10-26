from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, nullable=False)
    barkod = Column(String, unique=True, nullable=False)
    birim_fiyat = Column(Float, nullable=False)
    kdv_orani = Column(Float, nullable=False)
    stok_miktari = Column(Integer, nullable=False)
    skt = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
