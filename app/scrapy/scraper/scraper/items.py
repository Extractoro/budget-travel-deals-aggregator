# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookingHotel(scrapy.Item):
    title = scrapy.Field()
    address = scrapy.Field()
    distance = scrapy.Field()
    rating = scrapy.Field()
    amenities = scrapy.Field()
    old_price = scrapy.Field()
    current_price = scrapy.Field()
    taxes = scrapy.Field()

    def to_dict(self):
        return {
            'title': self.get('title'),
            'address': self.get('address'),
            'distance': self.get('distance'),
            'rating': self.get('rating'),
            'amenities': self.get('amenities'),
            'old_price': self.get('old_price'),
            'current_price': self.get('current_price'),
            'taxes': self.get('taxes')
        }
