import json
from urllib.parse import urlencode

import scrapy

from app.models.models import DataTypeEnum


class RyanairSpider(scrapy.Spider):
    name = "ryanair"
    data_type = DataTypeEnum.ONEWAY_FLIGHT
    allowed_domains = ["ryanair.com"]
    start_urls = ["https://ryanair.com"]

    def __init__(
            self,
            task_id=None,
            departure=None,
            arrival=None,
            date_from=None,
            date_to=None,
            currency=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.task_id = task_id
        self.departure = departure
        self.arrival = arrival
        self.date_from = date_from
        self.date_to = date_to
        self.currency = currency

    def get_query_parameters_dict(self):
        return {
            "departure": self.departure,
            "arrival": self.arrival,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "currency": self.currency,
        }

    def start_requests(self):
        base_url = "https://www.ryanair.com/api/farfnd/3/oneWayFares"
        params = {
            'departureAirportIataCode': self.departure,
            'arrivalAirportIataCode': self.arrival,
            'outboundDepartureDateFrom': self.date_from,
            'outboundDepartureDateTo': self.date_to,
            'currency': self.currency,
            'language': 'en',
        }
        url = f"{base_url}?{urlencode(params)}"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        fares = data.get("fares", [])
        for fare in fares:
            outbound = fare.get("outbound", {})
            departure_airport = outbound.get("departureAirport", {})
            arrival_airport = outbound.get("arrivalAirport", {})
            price_info = outbound.get("price", {})

            item = {
                "departure": departure_airport.get("name"),
                "arrival": arrival_airport.get("name"),
                "departureDate": outbound.get("departureDate"),
                "arrivalDate": outbound.get("arrivalDate"),
                "price": price_info.get("value"),
                "currency": price_info.get("currencyCode")
            }
            yield item
