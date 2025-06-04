import json

from celery.result import AsyncResult

from app.schemas.schemas import FilteringParams
from app.utils.sort_results import sort_results


def get_task_result_by_app(task_id: str, filtering: FilteringParams, celery_app):
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

        if isinstance(data, list):
            data = {'results': data}

        sort_results(data, filtering)

        return {"status": "success", "results": data["results"]}
    else:
        return {"status": task_result.state}


async def start_task(body, task_launcher_func):
    task_id = task_launcher_func(body)
    return {"task_id": task_id}
