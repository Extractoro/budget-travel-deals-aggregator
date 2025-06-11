from app.utils.wait_for_task_result import wait_for_task_result


def test_scrapy_oneway_fare(client):
    start_data = {
        "departure": "BER",
        "arrival": "BCN",
        "date_from": "2025-06-15",
        "date_to": "2025-06-18",
        "currency": "EUR"
    }

    response = client.post("/flights/oneway_fare/start", json=start_data)
    assert response.status_code == 200
    result = response.json()
    assert "task_id" in result
    task_id = result["task_id"]

    assert wait_for_task_result(task_id, max_retries = 30, delay = 2),\
    "Task failed or timeout"

    res = client.get(f"/flights/oneway_fare/{task_id}")
    assert res.status_code == 200

    data = res.json()
    assert "results" in data
    results = data["results"]
    assert isinstance(results, list)
    assert len(results) > 0

    item = results[0]
    assert "departure" in item
    assert "arrival" in item
    assert "departureDate" in item
    assert "arrivalDate" in item
    assert "price" in item
    assert "currency" in item


def test_search_flights_celery(client):
    data = {
        "originIata": "BER",
        "destinationIata": "BCN",
        "dateOut": "2025-06-15",
        "dateIn": "2025-06-18",
        "adults": 1,
        "teens": 0,
        "children": 0,
        "infants": 0,
        "isReturn": True,
        "discount": 0,
        "promoCode": "",
        "isConnectedFlight": False
    }

    response = client.post("/flights/search_flights/start", json=data)
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    assert wait_for_task_result(task_id, max_retries = 30, delay = 2),\
    "Task did not complete in time"

    res = client.get(f"/flights/search_flights/{task_id}")
    assert res.status_code == 200
    results = res.json()["results"]
    assert isinstance(results, list)
    assert len(results) > 0
