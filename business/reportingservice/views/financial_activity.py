# Third-party library imports
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from forexservice import models as currency_models
from paymentservice import models as payments_models
from ..serializers import (
    CurrencyExchangeSerializer,
    TransferRequestSerializer,
    TransactionRecordsSerializer
)


@register_permissions
@extend_schema(tags=["Reporting Services - Financial Activity"])
class UserFinancialActivityReportView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]

    # Method-specific permissions for implemented methods only
    get_permission = 'view_user_financial_activity'
    # required_permission = 'access_financial_reports'

    @extend_schema(
        request=None,
        responses=TransactionRecordsSerializer(many=True),
        operation_id="User Financial Activity Report",
        description="Retrieve financial activity report for the authenticated user."
    )
    def get(self, request):
        user = request.user

        # Fetch records belonging to the requesting user
        bureau_exchange_records = currency_models.CurrencyExchangeRecord.objects.filter(user=user)
        transfer_requests = payments_models.RequestedTransaction.objects.filter(
            models.Q(requesting_user=user) | models.Q(requested_user=user)
        )
        transaction_records = payments_models.TransactionRecord.objects.filter(
            models.Q(sender_wallet__wallet_owner=user) | models.Q(receiver_wallet__wallet_owner=user)
        )

        # Serialize response data with request context
        exchange_records = CurrencyExchangeSerializer(
            bureau_exchange_records, many=True, context={'request': request}
        ).data
        transfer_requests = TransferRequestSerializer(
            transfer_requests, many=True, context={'request': request}
        ).data
        transaction_records = TransactionRecordsSerializer(
            transaction_records, many=True, context={'request': request}
        ).data

        # Paginate each list individually
        paginator = LimitOffsetPagination()
        paginated_exchange_records = paginator.paginate_queryset(exchange_records, request)
        paginated_transfer_requests = paginator.paginate_queryset(transfer_requests, request)
        paginated_transaction_records = paginator.paginate_queryset(transaction_records, request)

        # Combine the paginated data
        data = {
            "exchange_records": paginated_exchange_records,
            "transfer_requests": paginated_transfer_requests,
            "transaction_records": paginated_transaction_records
        }

        # Return the paginated response
        return paginator.get_paginated_response(data)
