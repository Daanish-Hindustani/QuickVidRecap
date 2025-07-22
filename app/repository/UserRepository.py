from sqlalchemy.orm import Session
from ..model.Video import Videos
from ..schema.VideoSchema import VideoCreate, VideoUpdate

class VideoRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create
    def create(self, video_in: VideoCreate) -> Videos:
        video = Videos(**video_in.model_dump())
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video

    # Read
    def get_by_id(self, video_id: str) -> Videos | None:
        return self.db.query(Videos).filter(Videos.id == video_id).first()

    # noinspection PyTypeChecker
    def get_by_user_id(self, user_id: str) -> list[Videos]:
        return self.db.query(Videos).filter(Videos.user_id == user_id).all()

    # noinspection PyTypeChecker
    def list(self, skip: int = 0, limit: int = 100) -> list[Videos]:
        return self.db.query(Videos).offset(skip).limit(limit).all()

    # Update
    def update(self, video_id: str, video_update: VideoUpdate) -> Videos | None:
        video = self.get_by_id(video_id)
        if not video:
            return None

        update_data = video_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(video, key, value)

        self.db.commit()
        self.db.refresh(video)
        return video

    # Delete
    def delete(self, video_id: str) -> bool:
        video = self.get_by_id(video_id)
        if video:
            self.db.delete(video)
            self.db.commit()
            return True
        return False
