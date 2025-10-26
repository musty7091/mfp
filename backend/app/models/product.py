# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Float, Enum
from app.database import Base
import enum


class VatRateEnum(str, enum.Enum):
    zero = "0"
    reduced1 = "5"
    reduced2 = "10"
    medium = "16"
    standard = "20"
    special = "Özel Matrah"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    barcode = Column(String, nullable=True)
    unit_price = Column(Float, nullable=False)
    vat_rate = Column(Enum(VatRateEnum), default=VatRateEnum.standard)
