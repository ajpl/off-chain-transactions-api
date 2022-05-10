from decimal import Decimal

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from api import controller
from api.exceptions import (
    APIInsufficientFunds,
    APITickerMissmatch,
    APIUnknownBalance,
    InsufficientFunds,
    TickerMissmatch,
)
from api.models.balance import Balance
from api.models.balance_entry import BalanceEntry
from api.permissions import IsOwner
from api.serializers import BalanceEntrySerializer, BalanceSerializer


class BalanceList(generics.ListCreateAPIView):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsOwner]
    serializer_class = BalanceSerializer

    def get_queryset(self):
        return Balance.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BalanceDetail(generics.RetrieveAPIView):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsOwner]
    serializer_class = BalanceSerializer
    queryset = Balance.objects.all()


class BalanceEntryList(generics.ListCreateAPIView):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsOwner]
    serializer_class = BalanceEntrySerializer

    def get_queryset(self):
        return BalanceEntry.objects.filter(balance__owner=self.request.user)

    def create(self, request, *args, **kwargs):
        BalanceEntrySerializer(data=self.request.data).is_valid(raise_exception=True)
        balance = (
            Balance.objects.filter(owner=self.request.user)
            .filter(pk=self.request.data["balance"])
            .first()
        )
        if not balance:
            raise APIUnknownBalance
        balance_entry = None
        try:
            if balance:
                if (
                    int(self.request.data["tx_type"])
                    == BalanceEntry.TransactionType.AIRDROP.value
                ):
                    balance_entry = controller.airdrop(
                        self.request.data["balance"],
                        Decimal(str(self.request.data["tx_amount"])),
                    )
                if (
                    int(self.request.data["tx_type"])
                    == BalanceEntry.TransactionType.BURN.value
                ):
                    balance_entry = controller.burn(
                        self.request.data["balance"],
                        Decimal(str(self.request.data["tx_amount"])),
                    )
                if (
                    int(self.request.data["tx_type"])
                    == BalanceEntry.TransactionType.P2P.value
                ):
                    balance_entry = controller.p2p(
                        self.request.data["balance"],
                        self.request.data["to_balance"],
                        Decimal(str(self.request.data["tx_amount"])),
                    )
        except InsufficientFunds:
            raise APIInsufficientFunds
        except TickerMissmatch:
            raise APITickerMissmatch
        if balance_entry:
            serializer = BalanceEntrySerializer(balance_entry)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)


class BalanceEntryDetail(generics.RetrieveAPIView):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsOwner]
    serializer_class = BalanceEntrySerializer
    queryset = BalanceEntry.objects.all()
