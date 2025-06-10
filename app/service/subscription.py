from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Subscription, DataResults


def create_subscription(db: Session, task_id: str, user_id: int):
    if not db.query(DataResults).filter_by(task_id=task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")

    existing = db.query(Subscription).filter_by(user_id=user_id, task_id=task_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You are already subscribed to this task")

    subscription = Subscription(user_id=user_id, task_id=task_id)
    db.add(subscription)
    db.commit()


def delete_subscription(db: Session, task_id: str, user_id: int):
    if not db.query(DataResults).filter_by(task_id=task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")

    subscription = db.query(Subscription).filter_by(task_id=task_id, user_id=user_id).first()
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(subscription)
    db.commit()
