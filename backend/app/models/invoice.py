from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.schemas.invoice import InvoiceStatus # Önceki adımda tanımladığımız Enum

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    subtotal = Column(Float, default=0.0)
    vat_total = Column(Float, default=0.0)
    discount_total = Column(Float, default=0.0)
    grand_total = Column(Float, nullable=False)
    
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False)
    notes = Column(String, nullable=True)
    
    # İlişkiler
    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")
    
class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    description = Column(String, nullable=True)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)
    
    # Yeni eklenenler (KDV ve İskonto takibi için)
    discount_rate = Column(Float, default=0.0)
    line_total = Column(Float, nullable=False) # Kalem KDV dahil toplam tutarı

    # İlişkiler
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")