def test_register_user_success(test_client):
    response = test_client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_register_user_duplicate_username(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "pass123"
        }
    )
    response = test_client.post(
        "/api/auth/register",
        json={
            "username": "user1",
            "email": "dup@example.com",
            "password": "pass456"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exist."


def test_login_success(test_client):
    response = test_client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(test_client):
    response = test_client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_user_not_found(test_client):
    response = test_client.post(
        "/api/auth/login",
        data={"username": "nouser", "password": "testpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_get_current_user_success(test_client):
    login_response = test_client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )

    token = login_response.json()["access_token"]

    response = test_client.get(
        "/api/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_current_user_invalid_token(test_client):
    response = test_client.get(
        "/api/auth/users/me",
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    assert response.status_code == 401

def test_get_current_user_no_token(test_client):
    response = test_client.get("/api/auth/users/me")
    assert response.status_code == 401