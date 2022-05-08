from django.conf import settings
from django.core.serializers import serialize
from django.db import models

from api.fields.encrypted import EncryptedField


class Balance(models.Model):
    class Crypto(models.TextChoices):
        BITCOIN = "BTC", "Bitcoin"
        ETHEREUM = "ETH", "Ethereum"
        USDTETHER = "USDT", "USD Tether"
        LITECOIN = "LTC", "Litecoin"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )
    ticker = models.CharField(
        max_length=8,
        choices=Crypto.choices,
        default=Crypto.BITCOIN,
    )
    amount = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    hash = EncryptedField()
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_from_db()
        Balance.objects.filter(pk=self.pk).update(hash=self.get_json_bytes())

    def get_json_bytes(self, *args, **kwargs) -> bytes:
        return bytes(
            serialize(
                "json",
                [self],
                fields=("pk", "owner", "ticker", "amount", "created_at", "changed_at"),
            )[1:-1],
            "utf-8",
        )

    @property
    def is_trusted(self, *args, **kwargs) -> bool:
        if self.hash and self.hash == self.get_json_bytes():
            return True
        return False

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "ticker"], name="owner_ticker_pair"
            )
        ]
