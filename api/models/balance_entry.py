from django.db import models

from api.models.balance import Balance


class BalanceEntry(models.Model):
    class TransactionType(models.IntegerChoices):
        AIRDROP = 1, "Airdrop"
        BURN = 2, "Burn"
        P2P = 3, "P2P"

    balance = models.ForeignKey(Balance, on_delete=models.RESTRICT)
    tx_type = models.IntegerField(
        choices=TransactionType.choices, default=TransactionType.AIRDROP
    )
    tx_amount = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    amount_before_tx = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    amount_after_tx = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
