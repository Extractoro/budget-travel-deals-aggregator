from fastapi import APIRouter, Body, Query

from app.schemas.schemas import (RyanairFlightsSearch,
                                 RyanairOneWayFareBody,
                                 FilteringParams,
                                 AirlineSortEnum,
                                 SortOrder)
from app.service import flights as flights_service
from app.tasks import flight_tasks as flight_tasks
from app.utils.endpoint_task import start_task, get_task_result_by_app

router = APIRouter()


@router.post("/oneway_fare/start", tags=['Flights: Ryanair One-Way Fare'])
async def start_oneway_fare(body: RyanairOneWayFareBody = Body()):
    return await start_task(body, flights_service.get_oneway_fare_flight)


@router.get("/oneway_fare/{task_id}", tags=['Flights: Ryanair One-Way Fare'])
async def get_ryanair_task_result(task_id: str):
    return get_task_result_by_app(task_id, flight_tasks.run_ryanair_oneway_fare_spider.app)


@router.post("/search_flights/start", tags=['Flights: Ryanair Search Flights'])
async def start_search_flights(body: RyanairFlightsSearch = Body()):
    return await start_task(body, flights_service.get_search_flights)


@router.get("/search_flights/{task_id}", tags=['Flights: Ryanair Search Flights'])
async def get_search_task_result(
        task_id: str,
        airline_sort: AirlineSortEnum = Query(None),
        airline_sort_order: SortOrder = Query(SortOrder.asc)
):
    filtering = FilteringParams(airline_sort=airline_sort, airline_sort_order=airline_sort_order)
    return get_task_result_by_app(
        task_id,
        filtering,
        flight_tasks.run_ryanair_search_flights_spider.app)
