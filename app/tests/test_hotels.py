from app.utils.wait_for_task_result import wait_for_task_result


def test_search_hotels(client):
    start_data = {
        "destination": "Barcelona",
        "checkin": "2025-06-11",
        "checkout": "2025-06-12",
        "adults": 2,
        "rooms": 1,
        "children_ages": [5, 8]
    }

    response = client.post("/hotels/search_hotels/start", json=start_data)
    assert response.status_code == 200
    result = response.json()
    task_id = result["task_id"]
    assert task_id

    assert wait_for_task_result(task_id), "Celery task did not complete successfully in time"

    res = client.get(f"/hotels/search_hotels/{task_id}")
    assert res.status_code == 200

    data = res.json()
    assert "results" in data
    results = data["results"]
    assert isinstance(results, list)
    assert len(results) > 0

    hotel = results[0]
    assert "title" in hotel
    assert "address" in hotel
    assert "current_price" in hotel
    assert "taxes" in hotel
