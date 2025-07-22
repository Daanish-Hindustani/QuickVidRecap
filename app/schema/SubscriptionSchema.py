# schemas/subscription_schema.py (continued)

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class SubscriptionTypeEnum(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class SubscriptionCreate(BaseModel):
    subscription_type: SubscriptionTypeEnum
    subscription_start: datetime
    subscription_end: Optional[datetime] = None
    credits: int
    user_id: UUID


class SubscriptionUpdate(BaseModel):
    subscription_type: Optional[SubscriptionTypeEnum] = None
    subscription_start: Optional[datetime] = None
    subscription_end: Optional[datetime] = None
    credits: Optional[int] = None

    class Config:
        orm_mode = True


class SubscriptionResponse(BaseModel):
    id: int
    subscription_type: SubscriptionTypeEnum
    subscription_start: datetime
    subscription_end: Optional[datetime] = None
    credits: int
    user_id: UUID

    class Config:
        orm_mode = True
