# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import uuid

from app.database import SessionLocal
from app.models.models import DataResults


# useful for handling different item types with a single interface


class ScraperPipeline:
    def open_spider(self, spider):
        self.db = SessionLocal()
        self.collected_data = []
        self.task_id = spider.task_id

    def process_item(self, item, spider):
        self.collected_data.append(dict(item))
        return item

    def close_spider(self, spider):
        try:
            params_dict = spider.get_query_parameters_dict()
        except Exception:
            params_dict = {}

        try:
            result = DataResults(
                task_id=self.task_id,
                data_type=spider.data_type,
                data=self.collected_data,
                params=params_dict
            )
            self.db.add(result)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()
