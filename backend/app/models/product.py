from sqlalchemy import Column, Integer, String, Float, Enum
from app.database import Base
import enum

class VatRateEnum(float, enum.Enum):
    zero = 0.0        # %0
    low = 5.0         # %5
    medium = 10.0     # %10
    reduced = 16.0    # %16
    standard = 20.0   # %20
    special = -1.0    # Özel matrah (hesap dışı)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    barcode = Column(String, unique=True, nullable=True)
    unit_price = Column(Float, default=0.0)
    vat_rate = Column(Enum(VatRateEnum), default=VatRateEnum.standard)
