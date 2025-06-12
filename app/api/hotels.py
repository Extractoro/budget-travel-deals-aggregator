from fastapi import APIRouter, Body, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import DataTypeEnum
from app.schemas.schemas import (HotelsSearch,
                                 FilteringParams,
                                 HotelSortEnum,
                                 SortOrder,
                                 HotelTaskResult,
                                 TaskResponse)
from app.service import hotels as hotels_service
from app.utils.endpoint_task import start_task, get_task_result_by_app

router = APIRouter()


@router.post(
    "/search_hotels/start",
    tags=['Hotels: Search Hotels'],
    response_model=TaskResponse
)
async def start_search_hotels(body: HotelsSearch = Body()):
    return await start_task(body, hotels_service.get_search_hotel)


@router.get(
    "/search_hotels/{task_id}",
    tags=['Hotels: Search Hotels'],
    response_model=HotelTaskResult
)
async def get_search_task_result(
        task_id: str,
        hotel_sort: HotelSortEnum = Query(None),
        hotel_sort_order: SortOrder = Query(SortOrder.asc),
        db: Session = Depends(get_db)
):
    filtering = FilteringParams(hotel_sort=hotel_sort, hotel_sort_order=hotel_sort_order)
    return get_task_result_by_app(task_id, filtering, db, data_type=DataTypeEnum.HOTEL)
