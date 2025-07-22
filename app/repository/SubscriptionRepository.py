from sqlalchemy.orm import Session
from ..model.Subscription import Subscription
from ..schema.SubscriptionSchema import SubscriptionCreate, SubscriptionUpdate

class SubscriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create
    def create(self, sub_in: SubscriptionCreate) -> Subscription:
        subscription = Subscription(**sub_in.model_dump())
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    # Read by ID
    def get_by_id(self, subscription_id: int) -> Subscription | None:
        return self.db.query(Subscription).filter(Subscription.id == subscription_id).first()

    # Read all by user ID
    # noinspection PyTypeChecker
    def get_by_user_id(self, user_id: str) -> list[Subscription]:
        return self.db.query(Subscription).filter(Subscription.user_id == user_id).all()

    # Update
    def update(self, subscription_id: int, sub_update: SubscriptionUpdate) -> Subscription | None:
        subscription = self.get_by_id(subscription_id)
        if not subscription:
            return None

        update_data = sub_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(subscription, key, value)

        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    # Delete
    def delete(self, subscription_id: int) -> bool:
        subscription = self.get_by_id(subscription_id)
        if subscription:
            self.db.delete(subscription)
            self.db.commit()
            return True
        return False
