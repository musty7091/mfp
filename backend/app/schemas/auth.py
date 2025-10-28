from pydantic import BaseModel

# JWT Token yapısı
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Token'ın içerisindeki veri (Payload)
class TokenData(BaseModel):
    username: str | None = None