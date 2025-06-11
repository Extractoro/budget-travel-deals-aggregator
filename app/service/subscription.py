from datetime import datetime

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.models.models import Subscription, DataResults, DataTypeEnum
from app.schemas.schemas import FilteringParams
from app.utils.compare_data import compare_data
from app.utils.endpoint_task import get_task_result_by_app
from app.utils.run_spider_again import run_spider_again
from app.utils.send_email import send_email_alert
from app.utils.wait_for_task_result import wait_for_task_result


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


async def update_subscription_data(db: Session, old_data_result: DataResults, email: EmailStr):
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
        await send_email_alert(
            to_email=email,
            subject="🔔 Update by subscription",
            body="We found new offers for your request!"
        )

        old_data_result.data = new_data_result["results"]
        old_data_result.updated_at = datetime.utcnow()
        db.add(old_data_result)
    db.query(DataResults).filter_by(task_id=new_task_id).delete()

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    if not diff.get("has_changes"):
        diff["differences"] = "No changes found"

    return diff
