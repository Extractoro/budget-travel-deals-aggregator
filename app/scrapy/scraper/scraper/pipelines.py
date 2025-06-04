# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraperPipeline:
    def open_spider(self, spider):
        # self.file_path = 'hotels_output.json'
        # open(self.file_path, 'w').close()
        self.data = []

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item
