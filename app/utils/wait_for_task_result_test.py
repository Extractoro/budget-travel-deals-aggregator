from time import sleep


def wait_for_task_result_test(client, url_path: str, max_retries: int = 10, delay: float = 2.0):
    for _ in range(max_retries):
        res = client.get(url_path)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "SUCCESS":
                return True
        sleep(delay)
    return False
