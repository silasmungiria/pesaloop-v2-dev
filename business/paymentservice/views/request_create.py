# Standard library imports
import time

# Third-party library imports
from django.conf import settings
from django.db import OperationalError, transaction as db_transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Project-specific imports
from common import ReferenceGenerator
from rbac.permissions import MethodPermission, register_permissions
from walletservice import models as wallet_models
from userservice.models import User
from paymentservice.utils import RequestStatus, TransactionType
from paymentservice.models import RequestedTransaction
from paymentservice.serializers import (
    InitiateRequestSerializer,
    RequestedTransactionSerializer
)
from paymentservice.notifications import notify_transaction_request


@register_permissions
@extend_schema(tags=["Payment Service - Request"])
class RequestCreateView(APIView):
    """
    Handles payment requests between users via their wallets.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = InitiateRequestSerializer
    serializer_response_class = RequestedTransactionSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'create_payment_request'

    @extend_schema(
        request=InitiateRequestSerializer,
        responses=RequestedTransactionSerializer,
        operation_id="Create Payment Request",
        description="Endpoint for creating a payment request from one user's wallet to another user's wallet."
    )
    def post(self, request, *args, **kwargs):
        """
        Creates a payment request from one user's wallet to another user's wallet.
        """
        MAX_RETRIES = 3

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        requesting_user_id = request.user.id
        requested_user_id = serializer.validated_data['requested_user']
        request_amount = serializer.validated_data['request_amount']
        reason = serializer.validated_data.get('reason', None)

        if requesting_user_id == requested_user_id:
            return Response({"error": "You cannot request payment from yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request_amount <= 0:
            return Response({"error": "Amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(id__in=[requesting_user_id, requested_user_id])

        if users.count() < 2:
            return Response({"error": "Requester or requestee does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user_map = {user.id: user for user in users}

        requesting_user = user_map.get(requesting_user_id)
        requested_user = user_map.get(requested_user_id)

        try:
            with db_transaction.atomic():
                requester_wallet = wallet_models.DigitalWallet.objects.select_for_update().get(
                    wallet_owner=requesting_user, is_default=True
                )
        except wallet_models.DigitalWallet.DoesNotExist:
            return Response({"error": "Requester wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        for attempt in range(MAX_RETRIES):
            try:
                with db_transaction.atomic():
                    reference_id = ReferenceGenerator.payment_request_reference()

                    payment_request = RequestedTransaction.objects.create(
                        requesting_user=requesting_user,
                        requested_user=requested_user,
                        amount=request_amount,
                        currency=requester_wallet.currency.code,
                        reference_id=reference_id,
                        reason=reason,
                        transaction_type=TransactionType.INTERNAL_TRANSFER,
                        status=RequestStatus.PENDING,
                        payment_provider=settings.APP_NAME,
                    )

                db_transaction.on_commit(lambda: notify_transaction_request.delay(payment_request.id))

                return Response(self.serializer_response_class(payment_request).data, status=status.HTTP_201_CREATED)

            except OperationalError:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(0.1)
                    continue
                return Response({"error": "Database conflict, please retry the operation."}, status=status.HTTP_409_CONFLICT)

            except Exception as e:
                return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
