def test_get_profile(client):
    login_response = client.post(
        "/auth/login",
        json={"username": "user123", "password": "qwerty123"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/profile/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "user123"
