from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.dialects.mysql import CHAR

class Videos(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    private_url = Column(String(500), nullable=False)
    youtube_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    user = relationship("Users", backref="videos")
