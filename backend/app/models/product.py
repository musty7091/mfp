from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    unit = Column(String, default="Adet")
    price = Column(Float, nullable=False)
    vat = Column(Float, default=0.0)  # KDV oranı (örnek: 20.0)
