from fastapi import APIRouter, Body

from app.schemas.schemas import HotelsSearch
from app.service import hotels as hotels_service
from app.tasks import hotel_tasks as hotel_tasks
from app.utils.endpoint_task import start_task, get_task_result_by_app

router = APIRouter()


@router.post("/search_hotels/start", tags=['Hotels: Search Hotels'])
async def start_search_hotels(params: HotelsSearch = Body()):
    return await start_task(params, hotels_service.get_search_hotel)


@router.get("/search_hotels/{task_id}", tags=['Hotels: Search Hotels'])
async def get_search_task_result(task_id: str):
    return get_task_result_by_app(task_id, hotel_tasks.run_search_hotels_spider.app)
