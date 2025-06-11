from celery.result import AsyncResult
from time import sleep


def wait_for_task_result(task_id: str, max_retries: int = 10, delay: float = 5):
    result = AsyncResult(task_id)
    for _ in range(max_retries):
        if result.ready():
            if result.successful():
                return True
            else:
                return False
        sleep(delay)

    return False
