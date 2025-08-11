from django.urls import path
from .views import *

urlpatterns = [
    path('account/activities/', UserFinancialActivityReportView.as_view(), name='transaction-report'),
  
    path('transactions/download/', ExportTransactionStatementView.as_view(), name='transaction-statement'),
]