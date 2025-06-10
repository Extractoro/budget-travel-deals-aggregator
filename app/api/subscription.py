from datetime import datetime

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User, Subscription, DataResults, DataTypeEnum
from app.schemas.schemas import SubscriptionRequest, RyanairFlightsSearch, FilteringParams
from app.service.subscription import create_subscription, delete_subscription
from app.utils.compare_data import compare_data
from app.utils.endpoint_task import get_task_result_by_app
from app.utils.get_current_user import get_current_user
from app.utils.run_spider_again import run_spider_again
from app.utils.wait_for_task_result import wait_for_task_result

router = APIRouter()


@router.post("/subscribe", description="Subscribe on the task")
def subscribe_on_the_task(
    body: SubscriptionRequest = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    create_subscription(db, task_id=body.task_id, user_id=current_user.user_id)
    return {"message": "Subscribed successfully"}


@router.delete("/unsubscribe", description="Unsubscribe on the task")
def unsubscribe_on_the_task(
    body: SubscriptionRequest = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_subscription(db, task_id=body.task_id, user_id=current_user.user_id)
    return {"message": "Unsubscribed successfully"}


@router.post("/subscription/{task_id}/refresh")
async def refresh_subscription(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subscription = db.query(Subscription).filter_by(task_id=task_id, user_id=current_user.user_id).first()
    if not subscription:
        raise HTTPException(status_code=403, detail="Not subscribed")

    old_data_result = db.query(DataResults).filter_by(task_id=task_id).first()
    if not old_data_result:
        raise HTTPException(status_code=404, detail="Data not found")

    data_type = DataTypeEnum(old_data_result.data_type)
    params_dict = old_data_result.params

    new_task_id = await run_spider_again(data_type=data_type, params=params_dict)

    task_finished = wait_for_task_result(new_task_id)
    if not task_finished:
        raise HTTPException(status_code=504, detail="Task did not complete in time or failed")

    new_data_result = get_task_result_by_app(
        task_id=new_task_id,
        filtering=FilteringParams(),
        db=db,
        data_type=data_type
    )

    diff = compare_data(data_type, old_data_result.data, new_data_result['results'])

    if diff.get("has_changes"):
        old_data_result.data = new_data_result["results"]
        old_data_result.updated_at = datetime.utcnow()
        db.add(old_data_result)
    db.query(DataResults).filter_by(task_id=new_task_id).delete()
    db.commit()

    if not diff.get("has_changes"):
        diff["differences"] = "No changes found"

    return {
        "diff": diff,
    }
