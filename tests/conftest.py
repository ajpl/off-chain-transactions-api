import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True, scope="session")
def create_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return User.objects.create_user("test", password="123")


@pytest.fixture
def get_token(db):
    client = APIClient()
    response = client.post("/api/token/", data={"username": "test", "password": "123"})
    return response.json()["access"]
