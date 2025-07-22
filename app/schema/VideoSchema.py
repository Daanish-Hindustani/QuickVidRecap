# schemas/video_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class VideoCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    user_id: UUID
    youtube_url : str

class VideoResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    private_url: str
    youtube_url : str
    user_id: UUID

    class Config:
        orm_mode = True
