from sqlalchemy.orm import Session
from ..model.User import Users
from ..schema.UserSchema import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create
    def create(self, user_in: UserCreate) -> Users:
        user = Users(**user_in.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Read by ID
    def get_by_id(self, user_id: str) -> Users | None:
        return self.db.query(Users).filter(Users.id == user_id).first()

    # Read by email
    def get_by_email(self, email: str) -> Users | None:
        return self.db.query(Users).filter(Users.email == email).first()

    # Update
    def update(self, user_id: str, user_update: UserUpdate) -> Users | None:
        user = self.get_by_id(user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    # Delete
    def delete(self, user_id: str) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
