from pydantic import BaseModel, EmailStr

# Temel müşteri alanları
class CustomerBase(BaseModel):
    name: str
    contact_person: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    
    tax_number: str | None = None # Vergi numarası
    address: str | None = None

# Yeni müşteri oluşturmak için kullanılan şema
class CustomerCreate(CustomerBase):
    pass

# Müşteri verilerini okumak ve döndürmek için kullanılan şema
# NOT: Projenin başka yerlerinde CustomerResponse bekleniyor, bu yüzden bu adı kullanıyoruz.
class CustomerResponse(CustomerBase): 
    id: int # Veritabanı ID'si
    
    class Config:
        # Pydantic V2'de 'orm_mode' yerine 'from_attributes' kullanılır.
        # Altta çıkan UserWarning'ü gidermek için güncelleyelim.
        from_attributes = True

# Projenizin beklediği eski ad olan "Customer"ı da 
# yeni Response şemasına yönlendirerek geriye dönük uyumluluğu sağlıyoruz
Customer = CustomerResponse