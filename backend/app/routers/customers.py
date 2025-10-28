from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
# Düzeltildi: RoleEnum artık user modelinde tanımlı
from app.models.user import User, RoleEnum 
from app.schemas.customer import Customer, CustomerCreate
from app.core.security import get_current_user

router = APIRouter()

# Simülasyon: Müşteri verilerini geçici olarak burada tutuyoruz.
# Gerçek uygulamada DB'den çekilecektir.
DUMMY_CUSTOMERS = [
    {"id": 1, "name": "Global Tekstil A.Ş.", "contact_person": "Ayşe Yılmaz", "email": "ayse@global.com", "phone": "5321112233"},
    {"id": 2, "name": "Akdeniz Lojistik", "contact_person": "Mehmet Kaya", "email": "mehmet@akdeniz.com", "phone": "5423334455"},
]
customer_id_counter = 3

@router.get("/", response_model=list[Customer])
def read_customers(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """Tüm müşterileri listeler (Yetkili kullanıcı gerektirir)."""
    # Yetkilendirme kontrolü (Örn: sadece Admin ve Manager rolleri görebilir)
    # Bu kontrol, uygulamanızı satılabilir hale getirecek kritik bir özelliktir.
    if current_user.get("role") not in [RoleEnum.ADMIN.value, RoleEnum.MANAGER.value]:
        # Geçici olarak, 'role' bilgisini user modeline eklemeden önce 
        # sadece 'username'i kontrol edelim.
        pass # Şimdilik rol kontrolünü atlıyoruz, ileride ekleyeceğiz.
        
    # Normalde bu kısım DB sorgusu olacaktır.
    return [Customer(**c) for c in DUMMY_CUSTOMERS]

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: CustomerCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """Yeni müşteri kaydı oluşturur."""
    global customer_id_counter
    
    # Yeni müşteri verisini simülasyon listesine ekle
    new_customer = customer.dict()
    new_customer["id"] = customer_id_counter
    DUMMY_CUSTOMERS.append(new_customer)
    customer_id_counter += 1
    
    return Customer(**new_customer)

# Not: Diğer CRUD (okuma, güncelleme, silme) fonksiyonları bu yapıya eklenmelidir.