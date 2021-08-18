import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture()
def test_get_headers():
    token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBnbWFpbC5jb20iLCJleHAiOjE2MjkyODAzNDZ9.0_Bt2hH5y8WYOIdU5jA7GwxtE-UhAJbG7NlqtW-fLDM"
    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture()
def test_get_data():
    return {
        "email": "admin@gmail.com",
        "name": "admin",
        "is_admin": False,
        "id": 1,
        "hashed_password": "$2b$12$ZAVbtx9qIFjpIVOROioEkutbPnZLaC2aiyLXdqiQ4uLsYxQDAqaaq"
    }


@pytest.fixture()
def test_get_fake_headers():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1kZGluQGdtYWlsLmNvbSIsImV4cCI6MTYyOTI4MDM0Nn0.xcOhNB15PeOVYlSrmcvvZ5DyHZpj6qRuDpzmqATiQF0"
    }


@pytest.fixture()
def test_get_data_for_update():
    return {
        "email": "teststest@example.com",
        "name": "test",
        "is_admin": True,
        "hashed_password": "testtest"
    }
