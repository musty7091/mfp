from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import User, UserCreate
from app.core.security import get_current_user, admin_required, get_password_hash 

router = APIRouter(prefix="/users", tags=["Users"])

# Simülasyon: Kullanıcı verilerini geçici olarak burada tutuyoruz.
DUMMY_USERS = [
    User(id=1, username="admin", email="admin@mfp.com", is_active=True, is_admin=True),
]
user_id_counter = 2

@router.get("/", response_model=list[User], dependencies=[Depends(admin_required)])
def read_users(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """Tüm kullanıcıları listeler (Yalnızca Admin yetkisi gereklidir)."""
    # Gerçek DB sorgusu burada olacaktır.
    return DUMMY_USERS

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, 
             dependencies=[Depends(admin_required)])
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """Yeni kullanıcı kaydı oluşturur (Yalnızca Admin yetkisi gereklidir)."""
    global user_id_counter
    
    # Şifre hash'leme simülasyonu
    hashed_password = get_password_hash(user.password)
    
    new_user_dict = user.dict(exclude={'password'})
    new_user_dict.update({
        "id": user_id_counter,
        "hashed_password": hashed_password # DB modeline göre simülasyon
    })
    
    new_user = User(**new_user_dict)
    DUMMY_USERS.append(new_user)
    user_id_counter += 1
    
    return new_user