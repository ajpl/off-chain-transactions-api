from decimal import Decimal

from django.db import transaction

from api.exceptions import InsufficientFunds, TickerMissmatch
from api.models.balance import Balance
from api.models.balance_entry import BalanceEntry


def airdrop(id: int, amount: Decimal) -> BalanceEntry:

    with transaction.atomic():
        balance = Balance.objects.select_for_update().get(id=id)
        new_amount = balance.amount + amount
        balance_entry: BalanceEntry = BalanceEntry.objects.create(
            balance=balance,
            tx_type=BalanceEntry.TransactionType.AIRDROP,
            tx_amount=amount,
            amount_before_tx=balance.amount,
            amount_after_tx=new_amount,
        )

        balance.amount = new_amount
        balance.save()

    return balance_entry


def burn(id: int, amount: Decimal) -> Balance:
    with transaction.atomic():
        balance = Balance.objects.select_for_update().get(id=id)
        if balance.amount < amount:
            raise InsufficientFunds
        new_amount = balance.amount - amount
        balance_entry: BalanceEntry = BalanceEntry.objects.create(
            balance=balance,
            tx_type=BalanceEntry.TransactionType.BURN,
            tx_amount=amount,
            amount_before_tx=balance.amount,
            amount_after_tx=new_amount,
        )

        balance.amount = new_amount
        balance.save()

    return balance_entry


def p2p(from_id: int, to_id: int, amount: Decimal) -> Balance:
    with transaction.atomic():
        from_balance = Balance.objects.select_for_update().get(id=from_id)
        if from_balance.amount < amount:
            raise InsufficientFunds
        to_balance = Balance.objects.select_for_update().get(id=to_id)
        if from_balance.ticker != to_balance.ticker:
            raise TickerMissmatch

        from_new_amount = from_balance.amount - amount
        to_new_amount = to_balance.amount + amount
        balance_entry: BalanceEntry = BalanceEntry.objects.create(
            balance=from_balance,
            tx_type=BalanceEntry.TransactionType.P2P,
            to_balance=to_balance,
            tx_amount=amount,
            amount_before_tx=from_balance.amount,
            amount_after_tx=from_new_amount,
        )
        BalanceEntry.objects.create(
            balance=to_balance,
            tx_type=BalanceEntry.TransactionType.P2P,
            to_balance=from_balance,
            tx_amount=amount,
            amount_before_tx=to_balance.amount,
            amount_after_tx=to_new_amount,
        )
        from_balance.amount = from_new_amount
        from_balance.save()
        to_balance.amount = to_new_amount
        to_balance.save()

        return balance_entry
