import json

from celery.result import AsyncResult


def get_task_result_by_app(task_id: str, celery_app):
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state in ['PENDING', 'STARTED']:
        return {"status": "pending"}
    elif task_result.state == 'FAILURE':
        return {"status": "failure", "error": str(task_result.result)}
    elif task_result.state == 'SUCCESS':
        try:
            data = json.loads(task_result.result)
        except Exception:
            data = task_result.result
        return {"status": "success", "result": data}
    else:
        return {"status": task_result.state}


async def start_task(params, task_launcher_func):
    task_id = task_launcher_func(params)
    return {"task_id": task_id}