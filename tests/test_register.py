
from werkzeug.security import check_password_hash


def test_register_success(client):
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "SecurePassword123"
        }
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_register_missing_username(client):
    response = client.post(
        "/register",
        data={
            "username": "",
            "password": "SecurePassword123"
        }
    )

    assert response.status_code == 200
    assert b"Username and password are required." in response.data


def test_register_missing_password(client):
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": ""
        }
    )

    assert response.status_code == 200
    assert b"Username and password are required." in response.data


def test_register_duplicate_username(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "SecurePassword123"
        }
    )

    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "AnotherPassword123"
        }
    )

    assert response.status_code == 200
    assert b"Username already exists." in response.data

def test_register_get(client):
    response = client.get("/register")

    assert response.status_code == 200
    assert b"register" in response.data.lower()
