from app.schemas.schemas import HotelsSearch
from app.tasks.hotel_tasks import run_search_hotels_spider

def get_search_hotel(data: HotelsSearch):
    task = run_search_hotels_spider.delay(
        destination = data.destination,
        checkin = data.checkin,
        checkout = data.checkout,
        adults = data.adults,
        children_ages = data.children_ages,
        rooms = data.rooms,
        sort = data.sort,
    )
    return task.id