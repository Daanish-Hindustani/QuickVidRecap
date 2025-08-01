from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from enum import Enum as PyEnum
from .. db.database import Base
from datetime import datetime, timezone

class SubscriptionTypeEnum(PyEnum):
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_type = Column(Enum(SubscriptionTypeEnum), nullable=False)
    subscription_start = Column(DateTime, nullable=False)
    subscription_end = Column(DateTime, nullable=True)
    credits = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc) , onupdate=datetime.now(timezone.utc) )

    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
