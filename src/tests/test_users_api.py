def test_sign_up_user(client):
    response = client.post("/users/sign-up")
    assert response.status_code == 201
    assert response.json() is True
