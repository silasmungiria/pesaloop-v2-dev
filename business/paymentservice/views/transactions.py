# Third-party library imports
from django.db import models
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from paymentservice.models import TransactionRecord
from paymentservice.serializers import TransactionRecordSerializer


@register_permissions
@extend_schema(tags=["Payment Service - Records"])
class TransactionListView(APIView):
    """
    Retrieves transaction records for authenticated users.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = TransactionRecordSerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'list_transactions'

    @extend_schema(
        request=None,
        responses=TransactionRecordSerializer(many=True),
        operation_id="List Transactions",
        description="Endpoint for retrieving a list of transactions for the authenticated user."
    )
    def get(self, request, *args, **kwargs):
        transaction_id = request.query_params.get("id")
        reference_id = request.query_params.get("reference_id")
        request_user = request.user

        # Case: Fetch single transaction by ID
        if transaction_id:
            transaction_record = get_object_or_404(TransactionRecord, id=transaction_id)
            serializer = self.serializer_class(transaction_record)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Case: Fetch single transaction by reference_id
        if reference_id:
            transaction_record = get_object_or_404(TransactionRecord, reference_id=reference_id)
            serializer = self.serializer_class(transaction_record)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Case: Fetch all transactions for user
        transactions_qs = TransactionRecord.objects.filter(
            models.Q(sender_wallet__wallet_owner=request_user) |
            models.Q(receiver_wallet__wallet_owner=request_user)
        ).order_by("-created_at")

        # Annotate with transaction type (sent/received/unknown)
        transactions_qs = transactions_qs.annotate(
            type=models.Case(
                models.When(sender_wallet__wallet_owner=request_user, then=models.Value("sent")),
                models.When(receiver_wallet__wallet_owner=request_user, then=models.Value("received")),
                default=models.Value("unknown"),
                output_field=models.CharField(),
            )
        )

        # Use default pagination
        paginator = LimitOffsetPagination()
        paginated_transactions = paginator.paginate_queryset(transactions_qs, request)

        serializer = self.serializer_class(paginated_transactions, many=True)

        # Wrap in a dict while preserving paginated format
        wrapped_response = {
            "id": request_user.id,
            "full_name": request_user.get_full_name(),
            "email": request_user.email,
            "phone_number": request_user.phone_number,
            "transactions": serializer.data,
        }

        return paginator.get_paginated_response(wrapped_response)
