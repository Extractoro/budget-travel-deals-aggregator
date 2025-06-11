from fastapi import APIRouter, Body, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import DataTypeEnum
from app.schemas.schemas import (RyanairFlightsSearch,
                                 RyanairOneWayFareBody,
                                 FilteringParams,
                                 AirlineSortEnum,
                                 SortOrder, TaskResponse, RyanairOneFareTaskResult, RyanairFlightTaskResult)
from app.service import flights as flights_service
from app.utils.endpoint_task import start_task, get_task_result_by_app

router = APIRouter()


@router.post(
    "/oneway_fare/start",
    tags=['Flights: Ryanair One-Way Fare'],
    response_model=TaskResponse
)
async def start_oneway_fare(body: RyanairOneWayFareBody = Body()):
    return await start_task(body, flights_service.get_oneway_fare_flight)


@router.get(
    "/oneway_fare/{task_id}",
    tags=['Flights: Ryanair One-Way Fare'],
    response_model=RyanairOneFareTaskResult
)
async def get_ryanair_task_result(
        task_id: str,
        db: Session = Depends(get_db)
):
    filtering = FilteringParams()
    return get_task_result_by_app(task_id, filtering, db, data_type=DataTypeEnum.ONEWAY_FLIGHT)


@router.post(
    "/search_flights/start",
    tags=['Flights: Ryanair Search Flights'],
    response_model=TaskResponse
)
async def start_search_flights(body: RyanairFlightsSearch = Body()):
    return await start_task(body, flights_service.get_search_flights)


@router.get(
    "/search_flights/{task_id}",
    tags=['Flights: Ryanair Search Flights'],
    response_model=RyanairFlightTaskResult
)
async def get_search_task_result(
        task_id: str,
        airline_sort: AirlineSortEnum = Query(None),
        airline_sort_order: SortOrder = Query(SortOrder.asc),
        db: Session = Depends(get_db)
):
    filtering = FilteringParams(airline_sort=airline_sort, airline_sort_order=airline_sort_order)
    return get_task_result_by_app(task_id, filtering, db, data_type=DataTypeEnum.FLIGHT)
