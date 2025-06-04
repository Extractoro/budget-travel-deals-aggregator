import re

import scrapy

from ..items import BookingHotel


class HotelsSpider(scrapy.Spider):
    name = "hotels"
    allowed_domains = ["hotels.com"]
    start_urls = ["https://hotels.com"]

    def __init__(self, destination="Kyiv", checkin="2025-06-10", checkout="2025-06-11",
                 adults=1, rooms=1, children_ages=None, sort="RECOMMENDED", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = None
        self.destination = destination
        self.checkin = checkin
        self.checkout = checkout
        self.adults = adults
        self.rooms = rooms
        self.sort = sort

        if children_ages is None:
            self.children_ages = []
        elif isinstance(children_ages, str):
            self.children_ages = [int(x) for x in children_ages.split(",") if x.strip().isdigit()]
        else:
            raise ValueError("children_ages must be a list or None")

    def start_requests(self):
        item = BookingHotel()
        item['name'] = 'something'
        item['nightly_price'] = 'something'
        item['total_price'] = 'something'
        item['old_price'] = 'something'
        item['rating'] = 'something'
        item['amenities'] = 'something'
        yield item

        # base_url = "https://www.hotels.com/Hotel-Search"
        #
        # children_param = ",".join([f"1_{age}" for age in self.children_ages]) if self.children_ages else None
        #
        # self.params = {
        #     "destination": self.destination,
        #     "d1": self.checkin,
        #     "startDate": self.checkin,
        #     "d2": self.checkout,
        #     "endDate": self.checkout,
        #     "adults": self.adults,
        #     "rooms": self.rooms,
        #     "sort": self.sort,
        #     "useRewards": "false",
        # }
        #
        # if children_param:
        #     self.params["children"] = children_param
        #
        # url = f"{base_url}?{urlencode(self.params)}"
        #
        # self.logger.info(f"URL: {url}")
        # print(f"URL: {url}")
        #
        # yield scrapy.Request(
        #     url=url,
        #     meta={
        #         "playwright": True,
        #         "playwright_include_page": True,
        #         "playwright_browser_context_kwargs": {
        #             "proxy": {
        #                 "server": "http://proxy.scraperapi.com:8001",
        #                 "username": "scraperapi",
        #                 "password": SCRAPERAPI_KEY,
        #             }
        #         },
        #         "playwright_page_methods": [
        #             PageMethod("set_viewport_size", {"width": 1920, "height": 1080}),
        #             PageMethod("wait_for_selector", "div[data-stid='property-listing-results']", timeout=30000),
        #             # PageMethod("evaluate", """
        #             #     async () => {
        #             #         const delay = ms => new Promise(res => setTimeout(res, ms));
        #             #
        #             #         const scrollToBottom = async () => {
        #             #             let previousHeight = 0;
        #             #             let maxScrolls = 30;
        #             #             let scrolls = 0;
        #             #
        #             #             while (scrolls < maxScrolls) {
        #             #                 window.scrollTo(0, document.body.scrollHeight);
        #             #                 await delay(1500);
        #             #                 const currentHeight = document.body.scrollHeight;
        #             #                 if (currentHeight === previousHeight) break;
        #             #                 previousHeight = currentHeight;
        #             #                 scrolls++;
        #             #             }
        #             #         };
        #             #
        #             #         const clickShowMoreButtons = async () => {
        #             #             let maxClicks = 15;
        #             #             for (let i = 0; i < maxClicks; i++) {
        #             #                 const button = document.querySelector("button.uitk-button[type='button']:not([disabled])");
        #             #                 if (button && button.innerText.includes("Show more")) {
        #             #                     button.scrollIntoView();
        #             #                     button.click();
        #             #                     await delay(2000);
        #             #                 } else {
        #             #                     break;
        #             #                 }
        #             #             }
        #             #         };
        #             #
        #             #         await clickShowMoreButtons();
        #             #         await scrollToBottom();
        #             #     }
        #             # """),
        #             PageMethod("wait_for_timeout", 25000),
        #         ]
        #     },
        #     callback=self.parse_results
        # )

    def parse_results(self, response):
        self.logger.info("Parsing hotel results for: %s", self.destination)

        hotel_card = response.css(
            "div[data-stid='property-listing-results'] div[class='uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between']")

        def extract_price(text):
            if not text:
                return None
            match = re.search(r'([\d,\.]+)', text)
            if not match:
                return None
            cleaned = match.group(1).replace(',', '')
            try:
                return float(cleaned)
            except ValueError:
                return None

        results = []

        for hotel in hotel_card:
            nightly_price_text = hotel.xpath(
                ".//div[@data-test-id='price-summary-message-line']//div[contains(text(), 'nightly')]/text()"
            ).get()
            total_price_text = hotel.xpath(
                ".//div[@data-test-id='price-summary-message-line']//div[contains(text(), 'total')]/text()"
            ).get()
            old_price_text = hotel.css("del::text").get()

            nightly_price = extract_price(nightly_price_text)
            total_price = extract_price(total_price_text)
            old_price = extract_price(old_price_text)

            amenities = hotel.css("ul.uitk-typelist li div.uitk-text::text").getall()
            amenities = [a.strip() for a in amenities if a.strip()]

            results.append({
                "name": hotel.css("h3::text").get(),
                "nightly_price": nightly_price,
                "total_price": total_price,
                "old_price": old_price,
                "rating": hotel.css("span[class='uitk-badge-base-text'][aria-hidden='true']::text").get(),
                "amenities": amenities,
            })

            # yield item

        yield {
            "search_params": self.params,
            "url": response.url,
            "status": "success",
            "results": results,
        }
