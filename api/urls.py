from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

urlpatterns = [
    path("balances/", views.BalanceList.as_view()),
    path("balances/<int:pk>/", views.BalanceDetail.as_view()),
    path("balance-entries/", views.BalanceEntryList.as_view()),
    path("balance-entries/<int:pk>/", views.BalanceEntryDetail.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
