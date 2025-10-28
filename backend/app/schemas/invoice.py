from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from enum import Enum as PyEnum

# Fatura Kalemi Şeması (Fatura içindeki ürün/hizmet satırları)
class InvoiceItemBase(BaseModel):
    product_id: int = Field(..., description="Fatura edilen ürün/hizmet ID'si.")
    description: str = Field(..., description="Fatura kalemi açıklaması.")
    quantity: float = Field(..., gt=0, description="Miktar.")
    unit_price: float = Field(..., ge=0, description="Birim fiyatı (vergisiz).")
    tax_rate: float = Field(0.0, ge=0, description="Uygulanan KDV oranı (Örn: 0.18).")

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int
    total_amount: float = Field(..., description="Kalem toplam tutarı (KDV dahil).")
    
    class Config:
        from_attributes = True

# Fatura Durumları
class InvoiceStatus(PyEnum):
    DRAFT = "DRAFT"             # Taslak
    SENT = "SENT"               # Gönderildi (Tahsilat Bekliyor)
    PAID = "PAID"               # Tamamen Ödendi
    PARTIAL = "PARTIAL"         # Kısmen Ödendi
    CANCELED = "CANCELED"       # İptal Edildi

# Temel Fatura Şeması
class InvoiceBase(BaseModel):
    customer_id: int = Field(..., description="Faturanın kesildiği müşteri ID'si.")
    issue_date: date = Field(..., description="Fatura tarihi.")
    due_date: date = Field(..., description="Son ödeme tarihi.")
    status: InvoiceStatus = Field(InvoiceStatus.DRAFT, description="Fatura durumu.")
    notes: Optional[str] = None
    
# Yeni Fatura Oluşturma Şeması
class InvoiceCreate(InvoiceBase):
    # Fatura oluşturulurken kalemlerin listesi de gelir.
    items: List[InvoiceItemCreate]

# Fatura Güncelleme Şeması
class InvoiceUpdate(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[InvoiceStatus] = None
    notes: Optional[str] = None

# Fatura Okuma/Yanıt Şeması
class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str = Field(..., description="Sistem tarafından oluşturulan fatura numarası.")
    total_amount: float = Field(..., description="Fatura toplam tutarı (KDV dahil).")
    
    # İlişkisel veriler
    items: List[InvoiceItem] = Field([], description="Fatura kalemleri listesi.")
    
    class Config:
        from_attributes = True

# Projenin eski adlandırma beklentisine uyum için (ImportError'ı önler)
Invoice = InvoiceResponse