import json

from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from app.schemas.schemas import RyanairOneWayFareParams, RyanairFlightsSearch
from app.tasks import flight_tasks as flight_tasks
from app.service import flights as flights_service

router = APIRouter()


def get_task_result_by_app(task_id: str, celery_app):
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state in ['PENDING', 'STARTED']:
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


async def start_task(params, task_launcher_func):
    task_id = task_launcher_func(params)
    return {"task_id": task_id}

@router.get("/oneway_fare/start")
async def start_oneway_fare(params: RyanairOneWayFareParams = Depends()):
    return await start_task(params, flights_service.get_oneway_fare_flight)


@router.get("/oneway_fare/{task_id}")
async def get_ryanair_task_result(task_id: str):
    return get_task_result_by_app(task_id, flight_tasks.run_ryanair_oneway_fare_spider.app)


@router.get("/search_flights/start")
async def start_search_flights(params: RyanairFlightsSearch = Depends()):
    return await start_task(params, flights_service.get_search_flights)


@router.get("/search_flights/{task_id}")
async def get_search_task_result(task_id: str):
    return get_task_result_by_app(task_id, flight_tasks.run_ryanair_search_flights_spider.app)
