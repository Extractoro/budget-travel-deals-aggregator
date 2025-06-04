import os
import subprocess
import tempfile

from celery import shared_task


# def log_subprocess_output(pipe):
#     for line in iter(pipe.readline, b''):  # b'\n'-separated lines
#         logging.info('got line from subprocess: %r', line)


@shared_task
def run_ryanair_oneway_fare_spider(departure, arrival, date_from, date_to, currency):
    scrapy_project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'scrapy', 'scraper'))

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

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=scrapy_project_dir)

    return result.stdout


@shared_task(bind=True)
def run_ryanair_search_flights_spider(
        self,
        origin: str,
        destination: str,
        date_out: str,
        date_in: str = '',
        adults: int = 1,
        teens: int = 0,
        children: int = 0,
        infants: int = 0,
        is_return: bool = True,
        discount: int = 0,
        promo_code: str = '',
        is_connected_flight: bool = False
):
    scrapy_project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'scrapy', 'scraper'))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
        output_file = tf.name

    try:
        cmd = [
            "scrapy", "crawl", "ryanair_playwright",
            '-a', f'origin={origin}',
            '-a', f'destination={destination}',
            '-a', f'date_out={date_out}',
            '-a', f'date_in={date_in}',
            '-a', f'adults={adults}',
            '-a', f'teens={teens}',
            '-a', f'children={children}',
            '-a', f'infants={infants}',
            '-a', f'is_return={str(is_return).lower()}',
            '-a', f'discount={discount}',
            '-a', f'promo_code={promo_code}',
            '-a', f'is_connected_flight={str(is_connected_flight).lower()}',
            "-o", output_file,
        ]

        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=scrapy_project_dir)

        # process = Popen(cmd, text=True, cwd=scrapy_project_dir, stdout=PIPE, stderr=STDOUT)
        # with process.stdout:
        #     log_subprocess_output(process.stdout)
        # exitcode = process.wait()

        if proc.returncode != 0:
            raise Exception(f"Scrapy error: {proc.stderr}")

        with open(output_file, "r", encoding="utf-8") as f:
            result = f.read()

        return result

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)
