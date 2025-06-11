from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import DataResults, DataTypeEnum
from app.schemas.schemas import FilteringParams
from app.utils.sort_results import sort_results


def get_task_result_by_app(
        task_id: str,
        filtering: FilteringParams,
        db: Session,
        data_type: Optional[DataTypeEnum] = None
):
    query = db.query(DataResults).filter_by(task_id=task_id)
    if data_type:
        query = query.filter_by(data_type=data_type)

    result = query.first()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    response_data = {
        "task_id": task_id,
        "results": result.data
    }

    sort_results(response_data, filtering)
    return response_data


async def start_task(body, task_launcher_func):
    task_id = task_launcher_func(body)
    return {"task_id": task_id}
