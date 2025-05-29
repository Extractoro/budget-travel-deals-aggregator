import sys
import os
import importlib
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiders import Spider  # обязательно для issubclass

def run_spider(spider_name: str):
    spiders_path = os.path.join(os.path.dirname(__file__), 'spiders')

    available_spiders = [
        f[:-3] for f in os.listdir(spiders_path)
        if f.endswith('.py') and not f.startswith('__')
    ]

    if spider_name not in available_spiders:
        print(f"[❌] Spider '{spider_name}' not found. Available: {available_spiders}")
        return

    module_path = f"spiders.{spider_name}"
    spider_module = importlib.import_module(module_path)

    spider_class = None
    for attr in dir(spider_module):
        obj = getattr(spider_module, attr)
        if isinstance(obj, type) and issubclass(obj, Spider) and obj is not Spider:
            spider_class = obj
            break

    if spider_class is None:
        print(f"[❌] No Spider subclass found in {spider_name}.py")
        return

    output_file = f"{spider_name}_output.json"
    process = CrawlerProcess(settings={
        **get_project_settings(),
        "FEEDS": {
            output_file: {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "indent": 2,
            }
        }
    })

    print(f"[▶️] Starting spider '{spider_name}' → Output: {output_file}")
    process.crawl(spider_class)
    process.start()
    print(f"[✅] Spider '{spider_name}' finished. Results saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️  Usage: python starter.py <spider_name>")
    else:
        run_spider(sys.argv[1])

