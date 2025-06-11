import json

from app.utils.wait_for_task_result import wait_for_task_result


def test_subscription_flow(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    start_data = {
        "destination": "Kyiv",
        "checkin": "2025-06-15",
        "checkout": "2025-06-18",
        "adults": 1,
        "rooms": 1,
        "children_ages": []
    }

    res = client.post("/hotels/search_hotels/start", json=start_data)
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    assert wait_for_task_result(task_id, max_retries=30, delay=2), \
        "DataResults not populated in time"

    sub_res = client.post("/subscription/subscribe", json={"task_id": task_id}, headers=headers)
    assert sub_res.status_code == 200
    assert sub_res.json()["message"] == "Subscribed successfully"

    refresh_res = client.post(
        f"/subscription/{task_id}/refresh",
        json={"email": "user@example.com"},
        headers=headers
    )
    assert refresh_res.status_code == 200
    assert "diff" in refresh_res.json()

    unsub_res = client.request(
        method="DELETE",
        url="/subscription/unsubscribe",
        headers={**headers, "Content-Type": "application/json"},
        data=json.dumps({"task_id": task_id})
    )
    assert unsub_res.status_code == 200
    assert unsub_res.json()["message"] == "Unsubscribed successfully"
