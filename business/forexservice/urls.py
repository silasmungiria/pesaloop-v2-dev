from django.urls import path
from .views import *

urlpatterns = [
    path('exchange/preview/', ExchangePreviewView.as_view(), name='exchange-currency-preview'),
    path('exchange/execute/', ExchangeExecuteView.as_view(), name='exchange-currency-execute'),
   path('admin/exchange-rates/', AdminRatesView.as_view(), name='admin-exchange-rates'),
]
