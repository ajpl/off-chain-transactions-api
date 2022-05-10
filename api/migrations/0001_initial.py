# Generated by Django 3.2.13 on 2022-05-10 02:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import api.fields.encrypted


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Balance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ticker",
                    models.CharField(
                        choices=[
                            ("BTC", "Bitcoin"),
                            ("ETH", "Ethereum"),
                            ("USDT", "USD Tether"),
                            ("LTC", "Litecoin"),
                        ],
                        default="BTC",
                        max_length=8,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
                ("hash", api.fields.encrypted.EncryptedField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("changed_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BalanceEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tx_type",
                    models.IntegerField(
                        choices=[(1, "Airdrop"), (2, "Burn"), (3, "P2P")], default=1
                    ),
                ),
                (
                    "tx_amount",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
                (
                    "amount_before_tx",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
                (
                    "amount_after_tx",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "balance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="api.balance"
                    ),
                ),
                (
                    "to_balance",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="to_balance",
                        to="api.balance",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="balance",
            constraint=models.UniqueConstraint(
                fields=("owner", "ticker"), name="owner_ticker_pair"
            ),
        ),
    ]
