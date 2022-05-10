import factory


class BalanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "api.Balance"
