# app/schemas/__init__.py

# Müşteri Şemaları
from .customer import Customer, CustomerCreate, CustomerResponse

# Ürün Şemaları (Router'lar bunları bekliyor olabilir)
# Projenizdeki products.py router'ı ProductCreate, ProductResponse, ProductUpdate bekler.
from .product import Product, ProductCreate, ProductUpdate

# Fatura Şemaları
# Projenizdeki invoices.py router'ı InvoiceCreate, InvoiceResponse, InvoiceUpdate bekler.
from .invoice import Invoice, InvoiceCreate, InvoiceResponse, InvoiceUpdate

# Kullanıcı ve Yetkilendirme Şemaları
from .user import User, UserCreate
from .auth import Token, TokenData

# NOT: Bu dosya, app/schemas/product.py ve app/schemas/invoice.py 
# dosyalarının da var ve doğru içerikte olduğunu varsayar.
# Eğer bu dosyalar yoksa veya içerikleri hatalıysa, yeni hatalar alabiliriz.