from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User, Subscription, DataResults
from app.schemas.schemas import SubscriptionRequest, RefreshRequest, SubscriptionResult, SubscriptionDiffResponse
from app.service.subscription import (create_subscription,
                                      delete_subscription,
                                      update_subscription_data)
from app.utils.get_current_user import get_current_user

router = APIRouter()


@router.post(
    "/subscribe",
    description="Subscribe on the task",
    response_model=SubscriptionResult,
)
def subscribe_on_the_task(
        body: SubscriptionRequest = Body(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    create_subscription(db, task_id=body.task_id, user_id=current_user.user_id)
    return {"detail": "Subscribed successfully"}


@router.delete(
    "/unsubscribe",
    description="Unsubscribe on the task",
    response_model=SubscriptionResult
)
def unsubscribe_on_the_task(
        body: SubscriptionRequest = Body(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    delete_subscription(db, task_id=body.task_id, user_id=current_user.user_id)
    return {"detail": "Unsubscribed successfully"}


@router.post("/{task_id}/refresh", response_model=SubscriptionDiffResponse)
async def refresh_subscription(
        task_id: str,
        request: RefreshRequest = Body(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    subscription = (db.query(Subscription)
                    .filter_by(task_id=task_id, user_id=current_user.user_id)
                    .first())
    if not subscription:
        raise HTTPException(status_code=403, detail="Not subscribed")

    old_data_result = db.query(DataResults).filter_by(task_id=task_id).first()
    if not old_data_result:
        raise HTTPException(status_code=404, detail="Data not found")

    diff = await update_subscription_data(db, old_data_result, request.email)

    return {
        "diff": diff,
    }
