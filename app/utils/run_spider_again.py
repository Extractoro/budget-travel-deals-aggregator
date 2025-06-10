from app.schemas.schemas import HotelsSearch, RyanairFlightsSearch, RyanairOneWayFareBody
from app.service import hotels as hotels_service, flights as flights_service
from app.models.models import DataTypeEnum


async def run_spider_again(data_type: DataTypeEnum, params: dict):
    if data_type == DataTypeEnum.HOTEL:
        model = HotelsSearch(**params)
        return hotels_service.get_search_hotel(model)

    elif data_type == DataTypeEnum.FLIGHT:
        model = RyanairFlightsSearch(**params)
        return flights_service.get_search_flights(model)

    elif data_type == DataTypeEnum.ONEWAY_FLIGHT:
        model = RyanairOneWayFareBody(**params)
        return flights_service.get_oneway_fare_flight(model)

    else:
        raise ValueError(f"Unsupported data type: {data_type}")
