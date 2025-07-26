# schemas/video_schema.py
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class VideoCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    user_id: UUID
    youtube_url : str
    created_at: datetime
    updated_at: datetime

class VideoUpdate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    updated_at: datetime

class VideoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    private_url: str
    youtube_url : str
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
