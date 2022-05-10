import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

from api.models.balance import Balance
from tests.factories.balance import BalanceFactory


def test_cannot_have_two_balances_with_same_ticker(db, create_user):
    BalanceFactory(owner=create_user)
    with pytest.raises(IntegrityError):
        BalanceFactory(owner=create_user)


def test_can_have_two_tickers(db, create_user):
    BalanceFactory(owner=create_user)
    BalanceFactory(owner=create_user, ticker="ETH")
    assert Balance.objects.filter(owner=create_user).count() == 2


def test_get_balance_unauthenticated(api_client):
    response = api_client.get("/api/balances/")
    assert response.status_code == 401


def test_get_balance_list(api_client, get_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.get("/api/balances/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_balance_list_with_ticker(api_client, get_token, create_user):
    BalanceFactory(owner=create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.get("/api/balances/")
    assert response.status_code == 200
    assert response.json()[0]["ticker"] == "BTC"


def test_create_balance(api_client, get_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.post("/api/balances/", data={"ticker": "ETH"})
    assert response.status_code == 201
    assert response.json()["ticker"] == "ETH"


def test_create_balance_repeated(api_client, get_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    api_client.post("/api/balances/", data={"ticker": "ETH"})
    response = api_client.post("/api/balances/", data={"ticker": "ETH"})
    assert response.status_code == 400


def test_create_balance_invalid_ticker(api_client, get_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.post("/api/balances/", data={"ticker": "UST"})
    assert response.status_code == 400


def test_create_balance_without_auth(api_client):
    response = api_client.post("/api/balances/", data={"ticker": "ETH"})
    assert response.status_code == 401


def test_get_balance_resource(api_client, get_token, create_user):
    b = BalanceFactory(owner=create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.get(f"/api/balances/{b.id}/")
    assert response.status_code == 200
    assert response.json()["ticker"] == "BTC"


def test_get_balance_resource_without_auth(db, api_client, create_user):
    b = BalanceFactory(owner=create_user)
    response = api_client.get(f"/api/balances/{b.id}/")
    assert response.status_code == 401


def test_get_balance_resource_from_another_user(api_client, get_token):
    b = BalanceFactory(owner=User.objects.create_user("blabla"))
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.get(f"/api/balances/{b.id}/")
    assert response.status_code == 403
