from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    customer = "customer"
    representative = "representative"
    viewer = "viewer"

class UserBase(BaseModel):
    username: str
    email: str
    role: Optional[RoleEnum] = "customer"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True
