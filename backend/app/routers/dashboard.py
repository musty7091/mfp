from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user

router = APIRouter()

def get_dashboard_summary(db: Session):
    """Dashboard için metrikleri ve son faturaları simüle eder (Veritabanı bağlantısı henüz yapılmadı)."""

    # --- Simüle Edilmiş Metrikler ---
    metrics = {
        "monthly_revenue": 52350.50, # Son ayın cirosu
        "total_invoices": 135,
        "active_customers": 52
    }
    
    # --- Simüle Edilmiş Son Faturalar ---
    latest_invoices = [
        {"invoice_number": "INV-001", "customer_name": "Ali Market", "issue_date": "2025-10-25", "amount": 4500.00},
        {"invoice_number": "INV-002", "customer_name": "Beyza Ltd.", "issue_date": "2025-10-24", "amount": 2875.50},
        {"invoice_number": "INV-003", "customer_name": "Cem Ticaret", "issue_date": "2025-10-23", "amount": 1950.00},
        {"invoice_number": "INV-004", "customer_name": "Deniz Gıda", "issue_date": "2025-10-22", "amount": 8300.25},
        {"invoice_number": "INV-005", "customer_name": "Elif Tekstil", "issue_date": "2025-10-21", "amount": 3410.00},
    ]

    return {
        "metrics": metrics,
        "latest_invoices": latest_invoices
    }

@router.get("/dashboard/summary", status_code=status.HTTP_200_OK)
def read_dashboard_summary(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user) # Yetkilendirme kontrolü
):
    """Yönetim paneli özet verilerini döndürür."""
    # Simüle edilmiş veriler döndürülür
    return get_dashboard_summary(db)