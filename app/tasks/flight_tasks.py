import os
import subprocess

from celery import shared_task


@shared_task
def run_ryanair_spider(departure, arrival, date_from, date_to, currency):
    scrapy_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scrapy', 'scraper'))

    date_from_str = date_from.isoformat() if hasattr(date_from, 'isoformat') else str(date_from)
    date_to_str = date_to.isoformat() if hasattr(date_to, 'isoformat') else str(date_to)

    cmd = [
        "scrapy", "crawl", "ryanair",
        "-a", f"departure={departure}",
        "-a", f"arrival={arrival}",
        "-a", f"date_from={date_from_str}",
        "-a", f"date_to={date_to_str}",
        "-a", f"currency={currency}",
        '-o', '-:json'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=scrapy_project_dir)

    return result.stdout
