from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models.balance import Balance
from api.models.balance_entry import BalanceEntry


class BalanceSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Balance
        exclude = ["hash"]
        validators = [
            UniqueTogetherValidator(
                queryset=Balance.objects.all(), fields=["owner", "ticker"]
            )
        ]


class BalanceEntrySerializer(serializers.ModelSerializer):
    amount_before_tx = serializers.DecimalField(
        max_digits=18, decimal_places=8, read_only=True
    )
    amount_after_tx = serializers.DecimalField(
        max_digits=18, decimal_places=8, read_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    tx_type = serializers.IntegerField()

    def validate_tx_type(self, value):
        if value not in BalanceEntry.TransactionType.values:
            raise serializers.ValidationError("tx_type is not supported.")
        if (
            value == BalanceEntry.TransactionType.P2P.value
            and "to_balance" not in self.initial_data.keys()
        ):
            raise serializers.ValidationError(
                "to_balance field is required for P2P transactions."
            )

    class Meta:
        model = BalanceEntry
        exclude = []
        extra_kwargs = {
            "balance": {"required": True},
            "tx_type": {"required": True},
            "tx_amount": {"required": True},
        }
