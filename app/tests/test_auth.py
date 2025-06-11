def test_signup(client):
    # username = f"user_{uuid.uuid4().hex[:6]}"
    username = "user123"
    password = "qwerty123"

    response = client.post("/auth/signup", json={
        "username": username,
        "password": password
    })

    print(response.status_code, response.json())
    assert response.status_code == 200


def test_login(client):
    response = client.post("/auth/login", json={"username": "user123", "password": "qwerty123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
