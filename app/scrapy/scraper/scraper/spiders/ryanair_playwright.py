from urllib.parse import urlencode

import scrapy
from scrapy_playwright.page import PageMethod


class RyanairPlaywrightSpider(scrapy.Spider):
    name = "ryanair_playwright"
    allowed_domains = ["ryanair.com"]

    def __init__(
            self,
            origin='',
            destination='',
            date_out='',
            date_in='',
            adults='1',
            teens='0',
            children='0',
            infants='0',
            is_return='true',
            discount='0',
            promo_code='',
            is_connected_flight='false',
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.params = {
            'adults': adults,
            'teens': teens,
            'children': children,
            'infants': infants,
            'dateOut': date_out,
            'dateIn': date_in,
            'isConnectedFlight': is_connected_flight,
            'discount': discount,
            'promoCode': promo_code,
            'isReturn': is_return,
            'originIata': origin,
            'destinationIata': destination,
            'tpAdults': adults,
            'tpTeens': teens,
            'tpChildren': children,
            'tpInfants': infants,
            'tpStartDate': date_out,
            'tpEndDate': date_in,
            'tpDiscount': discount,
            'tpPromoCode': promo_code,
            'tpOriginIata': origin,
            'tpDestinationIata': destination,
        }

    def start_requests(self):
        base_url = "https://www.ryanair.com/us/en/trip/flights/select"
        url = f"{base_url}?{urlencode(self.params)}"
        yield scrapy.Request(
            url=url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "flight-card-new.flight-card", timeout=5000),
                ]
            },
            callback=self.parse_results
        )

    def parse_results(self, response):
        result = {
            "outbound": [],
            "inbound": []
        }

        def extract_price(flight):
            price = flight.css("span[data-e2e='flight-card-price'] flights-price-simple::text").get(default="").strip()
            return price if price else None

        outbound_container = response.css("journey-container[outbound]")
        outbound_flights = outbound_container.css("flight-card-new.flight-card")
        for flight in outbound_flights:
            result["outbound"].append({
                "airline": flight.css("div.flight-card__airline-label::text").get(default="").strip(),
                "flight_number": flight.css("div.card-flight-num__content::text").get(default="").strip(),
                "departure_time": flight.css(
                    "div[data-ref='flight-segment.departure'] > span.flight-info__hour::text").get(default="").strip(),
                "departure_city": flight.css(
                    "div[data-ref='flight-segment.departure'] > span.flight-info__city::text").get(default="").strip(),
                "arrival_time": flight.css("div[data-ref='flight-segment.arrival'] > span.flight-info__hour::text").get(
                    default="").strip(),
                "arrival_city": flight.css("div[data-ref='flight-segment.arrival'] > span.flight-info__city::text").get(
                    default="").strip(),
                "duration": flight.css("div[data-ref='flight_duration']::text").get(default="").strip(),
                "price": extract_price(flight),
            })

        inbound_container = response.css("journey-container[inbound]")
        inbound_flights = inbound_container.css("flight-card-new.flight-card")
        for flight in inbound_flights:
            result["inbound"].append({
                "airline": flight.css("div.flight-card__airline-label::text").get(default="").strip(),
                "flight_number": flight.css("div.card-flight-num__content::text").get(default="").strip(),
                "departure_time": flight.css(
                    "div[data-ref='flight-segment.departure'] > span.flight-info__hour::text").get(default="").strip(),
                "departure_city": flight.css(
                    "div[data-ref='flight-segment.departure'] > span.flight-info__city::text").get(default="").strip(),
                "arrival_time": flight.css("div[data-ref='flight-segment.arrival'] > span.flight-info__hour::text").get(
                    default="").strip(),
                "arrival_city": flight.css("div[data-ref='flight-segment.arrival'] > span.flight-info__city::text").get(
                    default="").strip(),
                "duration": flight.css("div[data-ref='flight_duration']::text").get(default="").strip(),
                "price": extract_price(flight),
            })

        yield result

