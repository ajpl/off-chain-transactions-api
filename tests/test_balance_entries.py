from django.contrib.auth.models import User

from tests.factories.balance import BalanceFactory


def test_get_balance_entries_unauthenticated(api_client):
    response = api_client.get("/api/balance-entries/")
    assert response.status_code == 401


def test_get_balance_entries_list(api_client, get_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.get("/api/balance-entries/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_balance_entries_list_one_entry(api_client, get_token, create_user):
    b = BalanceFactory(owner=create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    api_client.post(
        "/api/balance-entries/", data={"balance": b.id, "tx_amount": 1.25, "tx_type": 1}
    )
    response = api_client.get("/api/balance-entries/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_balance_entry(api_client, get_token, create_user):
    b = BalanceFactory(owner=create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    be = api_client.post(
        "/api/balance-entries/", data={"balance": b.id, "tx_amount": 1.50, "tx_type": 1}
    )
    response = api_client.get(f"/api/balances/{b.id}/")
    assert be.status_code == 201
    assert be.json()["amount_before_tx"] == "0.00000000"
    assert be.json()["amount_after_tx"] == "1.50000000"
    assert response.status_code == 200
    assert response.json()["amount"] == "1.50000000"


def test_create_balance_entry_without_auth(db, api_client, create_user):
    b = BalanceFactory(owner=create_user)
    response = api_client.post(
        "/api/balance-entries/", data={"balance": b.id, "tx_amount": 1.50, "tx_type": 1}
    )
    assert response.status_code == 401


def test_create_balance_entry_without_ownership(api_client, get_token, create_user):
    BalanceFactory(owner=create_user)
    b2 = BalanceFactory(owner=User.objects.create_user("blablabla"))
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.post(
        "/api/balance-entries/",
        data={"balance": b2.id, "tx_amount": 1.50, "tx_type": 1},
    )
    assert response.status_code == 403


def test_create_balance_entries(api_client, get_token, create_user):
    b = BalanceFactory(owner=create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    be1 = api_client.post(
        "/api/balance-entries/", data={"balance": b.id, "tx_amount": 1.50, "tx_type": 1}
    )
    assert be1.status_code == 201
    assert be1.json()["amount_before_tx"] == "0.00000000"
    assert be1.json()["amount_after_tx"] == "1.50000000"
    be2 = api_client.post(
        "/api/balance-entries/", data={"balance": b.id, "tx_amount": 0.5, "tx_type": 2}
    )
    assert be2.status_code == 201
    assert be2.json()["amount_before_tx"] == "1.50000000"
    assert be2.json()["amount_after_tx"] == "1.00000000"
    response = api_client.get(f"/api/balances/{b.id}/")
    assert response.status_code == 200
    assert response.json()["amount"] == "1.00000000"


def test_create_balance_entry_insufficient_funds_burn(
    api_client, get_token, create_user
):
    b = BalanceFactory(owner=create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.post(
        "/api/balance-entries/", data={"balance": b.id, "tx_amount": 1.50, "tx_type": 2}
    )
    assert response.status_code == 422


def test_create_balance_entry_insufficient_funds_p2p(
    api_client, get_token, create_user
):
    b = BalanceFactory(owner=create_user)
    b2 = BalanceFactory(owner=create_user, ticker="ETH")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    response = api_client.post(
        "/api/balance-entries/",
        data={"balance": b.id, "tx_amount": 1.50, "tx_type": 3, "to_balance": b2.id},
    )
    assert response.status_code == 422


def test_create_balance_entry_ticker_missmatch(api_client, get_token, create_user):
    b = BalanceFactory(owner=create_user)
    b2 = BalanceFactory(owner=create_user, ticker="ETH")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token}")
    api_client.post(
        "/api/balance-entries/", data={"balance": b.id, "tx_amount": 1.50, "tx_type": 1}
    )
    response = api_client.post(
        "/api/balance-entries/",
        data={"balance": b.id, "tx_amount": 1.50, "tx_type": 3, "to_balance": b2.id},
    )
    assert response.status_code == 400
