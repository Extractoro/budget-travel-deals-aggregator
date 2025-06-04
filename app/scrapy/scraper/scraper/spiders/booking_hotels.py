from urllib.parse import urlencode

import scrapy

from ..items import BookingHotel
from app.utils.parse_fields import parse_price
from app.utils.safe_strip import safe_strip


class BookingHotelsSpider(scrapy.Spider):
    name = "booking_hotels"
    allowed_domains = ["booking.com"]
    start_urls = ["https://booking.com"]

    def __init__(self,
                 destination="Kyiv",
                 checkin="2025-06-10",
                 checkout="2025-06-11",
                 adults=1,
                 rooms=1,
                 children_ages=None,
                 lang="en-gb",
                 selected_currency='USD',
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.destination = destination
        self.checkin = checkin
        self.checkout = checkout
        self.adults = adults
        self.rooms = rooms
        self.lang = lang
        self.selected_currency = selected_currency

        if children_ages is None:
            self.children_ages = []
        elif isinstance(children_ages, str):
            self.children_ages = [int(x) for x in children_ages.split(",") if x.strip().isdigit()]
        elif isinstance(children_ages, list):
            self.children_ages = children_ages
        else:
            raise ValueError("children_ages must be a list, a comma-separated string, or None")

        self.children_count = len(self.children_ages)

    def get_search_params(self):
        params = [
            ("ss", self.destination),
            ("checkin", self.checkin),
            ("checkout", self.checkout),
            ("group_adults", str(self.adults)),
            ("no_rooms", str(self.rooms)),
            ("group_children", str(self.children_count)),
            ("lang", self.lang),
            ("selected_currency", self.selected_currency),
        ]

        for age in self.children_ages:
            params.append(("age", str(age)))

        return params

    def start_requests(self):
        """
        https://www.booking.com/searchresults.en-gb.html
        ?ss=Kyiv
        &lang=en-gb
        &checkin=2025-06-06
        &checkout=2025-06-11
        &group_adults=1
        &no_rooms=1
        &group_children=2&age=3&age=10
        """
        base_url = "https://www.booking.com/searchresults.en-gb.html"
        query_string = urlencode(self.get_search_params(), doseq=True)
        url = f"{base_url}?{query_string}"

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hotel_card = response.xpath('//div[@data-testid="property-card"]')

        for hotel in hotel_card:
            item = BookingHotel()
            item['title'] = safe_strip(hotel.xpath('.//div[@data-testid="title"]/text()'))
            item['address'] = safe_strip(hotel.xpath('.//span[@data-testid="address"]/text()'))
            item['distance'] = safe_strip(hotel.xpath('.//span[@data-testid="distance"]/text()'))
            rating_str  = safe_strip(
                hotel.xpath('.//div[@data-testid="review-score"]//div[@aria-hidden="true"]/text()'))
            try:
                item['rating'] = float(rating_str) if rating_str else None
            except ValueError:
                item['rating'] = None
            item['amenities'] = [a.strip() for a in hotel.xpath(
                './/div[@data-testid="property-card-unit-configuration"]/span/text()').getall()]
            item['old_price'] = parse_price(safe_strip(hotel.xpath('.//span[contains(@class, "d68334ea31")]/text()')))
            item['current_price'] = parse_price(safe_strip(hotel.xpath('.//span[@data-testid="price-and-discounted-price"]/text()')))
            item['taxes'] = safe_strip(hotel.xpath('.//div[@data-testid="taxes-and-charges"]/text()'))

            yield item
