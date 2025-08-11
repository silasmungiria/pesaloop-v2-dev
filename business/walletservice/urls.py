from django.urls import path
from .views import (
    CurrencyView,
    CurrencyDetailView,
    ListWalletsView,
    SetDefaultWalletView,
    ActivateWalletView,
    DevelopmentWalletTopUpView
)

urlpatterns = [
    # Currency Management
    path('currencies/', CurrencyView.as_view(), name='list-create-currencies'),
    path('currencies/<uuid:id>/', CurrencyDetailView.as_view(), name='currency-detail'),

    # Wallet Management
    path('wallets/', ListWalletsView.as_view(), name='list-wallets'),
    path('wallets/<uuid:id>/set-default/', SetDefaultWalletView.as_view(), name='set-default-wallet'),
    path('wallets/<uuid:id>/activate/', ActivateWalletView.as_view(), name='activate-wallet'),

    # Developer Wallets
    path('developer/wallets/top-up', DevelopmentWalletTopUpView.as_view(), name='list-developer-wallets'),
]
