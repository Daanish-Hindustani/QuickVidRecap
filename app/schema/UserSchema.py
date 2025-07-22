from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    phone_number: str
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    updated_at: Optional[datetime] = None

class UserResponse(UserBase):
    id: UUID

    class Config:
        orm_mode = True
