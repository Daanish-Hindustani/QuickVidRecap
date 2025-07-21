from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    phone_number: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

class UserOut(UserBase):
    id: UUID

    class Config:
        orm_mode = True
