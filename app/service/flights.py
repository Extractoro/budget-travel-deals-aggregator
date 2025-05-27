from app.schemas.schemas import FlightsGetParams
from app.tasks.flight_tasks import run_ryanair_spider


def get_flights(data: FlightsGetParams):
    task = run_ryanair_spider.delay(
        departure=data.departure,
        arrival=data.arrival,
        date_from=data.date_from,
        date_to=data.date_to,
        currency=data.currency,
    )
    return task.id
