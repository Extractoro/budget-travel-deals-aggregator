import re

import scrapy

from scrapy_playwright.page import PageMethod


class HotelsSpider(scrapy.Spider):
    name = "hotels"
    allowed_domains = ["hotels.com"]
    start_urls = ["https://hotels.com"]

    def __init__(self, destination="Kyiv", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destination = destination

    def start_requests(self):
        self.logger.info(f"Запуск запроса для: {self.destination}")
        yield scrapy.Request(
            url="https://www.hotels.com/",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("add_init_script",
                               "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"),
                    PageMethod("click", "button[aria-label='Where to?']"),
                    PageMethod("wait_for_selector", "input[id='destination_form_field']"),
                    PageMethod("fill",
                               "input[id='destination_form_field'][aria-label='Where to?']",
                               self.destination),
                    PageMethod("wait_for_selector", "ul[role='list'] li"),
                    PageMethod("click", "ul[role='list'] li:nth-child(1)"),
                    PageMethod("wait_for_selector", "button[id='search_button'][type='submit']"),
                    PageMethod("click", "button[id='search_button'][type='submit']"),
                    PageMethod("wait_for_selector", "div[data-stid='property-listing-results']", timeout=10000),
                    PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_timeout", 3000),
                ]
            },
            callback=self.parse_results
        )

    def parse_results(self, response):
        self.logger.info("Parsing hotel results for: %s", self.destination)
        hotel_card = response.css(
            "div[data-stid='property-listing-results'] div[class='uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between']")

        def extract_price(text):
            if not text:
                return None
            match = re.search(r"\$([\d,.]+)", text)
            return int(match.group(1)) if match else None

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

            yield {
                "name": hotel.css("h3::text").get(),
                "nightly_price": nightly_price,
                "total_price": total_price,
                'old_price': old_price,
                "rating": hotel.css("span[class='uitk-badge-base-text'][aria-hidden='true']::text").get(),
                "amenities": amenities,
            }
