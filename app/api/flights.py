import json

from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from app.schemas.schemas import FlightsGetParams
from app.tasks import flight_tasks as flight_tasks
from app.service import flights as flights_service

router = APIRouter()


@router.get("/start")
async def start_flight_task(params: FlightsGetParams = Depends()):
    task_id = flights_service.get_flights(params)
    return {"task_id": task_id}


@router.get("/{task_id}")
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=flight_tasks.run_ryanair_spider.app)

    if task_result.state == 'PENDING' or task_result.state == 'STARTED':
        return {"status": "pending"}
    elif task_result.state == 'FAILURE':
        return {"status": "failure", "error": str(task_result.result)}
    elif task_result.state == 'SUCCESS':
        try:
            data = json.loads(task_result.result)
        except Exception:
            data = task_result.result
        return {"status": "success", "result": data}
    else:
        return {"status": task_result.state}
