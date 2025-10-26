from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    barcode = Column(String(50), unique=True, nullable=False)   # Barkod alanı
    vat_rate = Column(Float, nullable=False, default=0.05)      
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    expiry_date = Column(Date, nullable=True)                   # Son kullanma tarihi
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', barcode='{self.barcode}', price={self.price}, stock={self.stock})>"
