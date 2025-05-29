import os
import subprocess
import tempfile
from typing import Optional

from celery import shared_task

@shared_task(bind=True)
def run_search_hotels_spider(
        self,
        destination: str,
        checkin: str,
        checkout: str,
        adults: int,
        children_ages: Optional[list],
        rooms: int,
        sort: str,
):
    allowed_sort_values = {"RECOMMENDED", "PRICE_LOW_TO_HIGH", "PRICE_HIGH_TO_LOW"}
    if sort not in allowed_sort_values:
        raise ValueError(f"Invalid sort value: {sort}. Allowed: {', '.join(allowed_sort_values)}")

    if children_ages is not None:
        if not isinstance(children_ages, list):
            raise ValueError("children_ages must be a list")
        for age in children_ages:
            if not isinstance(age, int) or not (0 <= age <= 17):
                raise ValueError(f"Invalid child age: {age}. Acceptable ages are 0 to 17.")

    scrapy_project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'scrapy', 'scraper'))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
        output_file = tf.name

    try:
        cmd = [
            "scrapy", "crawl", "hotels",
            '-a', f'destination={destination}',
            '-a', f'checkin={checkin}',
            '-a', f'checkout={checkout}',
            '-a', f'adults={adults}',
            '-a', f'rooms={rooms}',
            '-a', f'sort={sort}',
            "-o", output_file,
        ]

        if children_ages is not None:
            cmd.append(f"-a")
            cmd.append(f"children_ages={','.join(map(str, children_ages))}")

        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=scrapy_project_dir)

        if proc.returncode != 0:
            raise Exception(f"Scrapy error: {proc.stderr}")

        with open(output_file, "r", encoding="utf-8") as f:
            result = f.read()

        return result

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)
