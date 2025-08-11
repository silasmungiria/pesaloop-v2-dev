from django.urls import path
from .views import *


urlpatterns = [
    # Recipient Verification
    path('recipient/verify/', VerifyRecipientView.as_view(), name='verify-recipient'),

    # Transactions (Sent / Received)
    path('transactions/', TransactionListView.as_view(), name='list-transactions'),
    path('transactions/initiate/', TransferCreateView.as_view(), name='create-transaction'),

    # Transfer Requests (Request money)
    path('transfer-requests/', RequestListView.as_view(), name='list-transfer-requests'),
    path('transfer-requests/initiate/', RequestCreateView.as_view(), name='create-transfer-request'),
    path('transfer-requests/action/', ProcessPaymentRequestView.as_view(), name='process-transfer-request'),
]
