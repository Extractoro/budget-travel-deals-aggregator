from app.schemas.schemas import RyanairOneWayFareBody, RyanairFlightsSearch
from app.tasks.flight_tasks import run_ryanair_oneway_fare_spider, run_ryanair_search_flights_spider


def get_oneway_fare_flight(data: RyanairOneWayFareBody):
    task = run_ryanair_oneway_fare_spider.delay(
        departure=data.departure,
        arrival=data.arrival,
        date_from=data.date_from,
        date_to=data.date_to,
        currency=data.currency,
    )
    return task.id


def get_search_flights(data: RyanairFlightsSearch):
    task = run_ryanair_search_flights_spider.delay(
        origin=data.origin,
        destination=data.destination,
        date_out=data.date_out,
        date_in=data.date_in if data.is_return else '',
        adults=data.adults,
        teens=data.teens,
        children=data.children,
        infants=data.infants,
        is_return=data.is_return,
        # discount=data.discount,
        # promo_code=data.promo_code,
        # is_connected_flight=data.is_connected_flight,
    )
    return task.id
