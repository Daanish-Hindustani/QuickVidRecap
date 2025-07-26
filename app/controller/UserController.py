from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schema.UserSchema import UserCreate, UserUpdate, UserResponse
from app.schema.VideoSchema import VideoResponse  # <-- Make sure this is imported
from app.repository.UserRepository import UserRepository
from app.db.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# Create User
@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return repo.create(user)

# Get User
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update User
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    existing_user = repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = repo.update(user_id, user_update)
    return updated_user

# Delete User
@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return repo.delete(user_id)

# Get User Videos
@router.get("/{user_id}/videos", response_model=List[VideoResponse])
async def get_videos(user_id: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.videos
