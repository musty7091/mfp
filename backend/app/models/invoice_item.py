from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    discount_rate = Column(Float)
    unit_price = Column(Float)
    vat_rate = Column(Float)
    line_total = Column(Float)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")
