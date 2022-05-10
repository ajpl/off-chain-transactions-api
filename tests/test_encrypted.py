from decimal import Decimal

from freezegun import freeze_time

from api.models.balance import Balance


@freeze_time("2022-09-07 12:00:01")
def test_is_trusted_ok(db, create_user):
    balance = Balance.objects.create(owner=create_user, ticker="ETH")
    balance.refresh_from_db()
    unencrypted_hash = b'{"model": "api.balance", "pk": 1, "fields": {"owner": 1, "ticker": "ETH", "amount": "0E-8", "created_at": "2022-09-07T12:00:01Z", "changed_at": "2022-09-07T12:00:01Z"}}'  # noqa: E501
    assert balance.hash == unencrypted_hash
    assert balance.is_trusted


def test_is_trusted_fail_modified_model(db, create_user):
    balance = Balance.objects.create(owner=create_user, ticker="ETH")
    balance.refresh_from_db()
    balance.amount = Decimal(10)
    assert not balance.is_trusted
    assert balance.hash
