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
from paymentservice.models import RequestedTransaction, TransactionRecord
from paymentservice.serializers import (
  TransferRequestActionSerializer,
  TransactionRecordSerializer,
  RequestedTransactionSerializer
)
from paymentservice.services import TransactionFeeCalculator
from paymentservice.utils import (
  RequestAction,
  RequestStatus,
  TransactionType,
  TransactionStatus,
  TransferLimits
)
from paymentservice.notifications import (
  notify_transaction_approval,
  notify_transaction_cancellation
)


TRANSFER_LIMIT = TransferLimits.UNVERIFIED_WALLET_MAX_TRANSFER


@register_permissions
@extend_schema(tags=["Payment Service - Request"])
class ProcessPaymentRequestView(APIView):
    """
    Handles approval or cancellation of a payment request by the requestee.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = TransferRequestActionSerializer
    serializer_response_class = TransactionRecordSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'process_payment_request'

    MAX_RETRIES = 3

    @extend_schema(
        request=TransferRequestActionSerializer,
        responses=RequestedTransactionSerializer,
        operation_id="Process Payment Request",
        description="Endpoint for processing a payment request by approving or cancelling it or declining it."
    )
    def post(self, request, *args, **kwargs):
        """Handles approval or cancellation of a payment request."""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user
        request_id = serializer.validated_data['request_id']
        action = serializer.validated_data['action']

        if action not in dict(RequestAction.CHOICES).keys():
            return Response(
                {"error": f"Invalid action: {action}. Valid actions are: {', '.join(dict(RequestAction.CHOICES).keys())}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        for attempt in range(self.MAX_RETRIES):
            try:
                with db_transaction.atomic():
                    payment_request = RequestedTransaction.objects.select_for_update().get(id=request_id)

                    if payment_request.status in [RequestStatus.SUCCESS, RequestStatus.CANCELLED, RequestStatus.DECLINED]:
                        return Response(
                            {"error": "This payment request has already been processed."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    if action == RequestAction.APPROVE:
                        return self._approve_payment_request(payment_request, current_user)
                    elif action == RequestAction.CANCEL:
                        return self._cancel_payment_request(payment_request, current_user)

            except RequestedTransaction.DoesNotExist:
                return Response({"error": "Payment request not found."}, status=status.HTTP_404_NOT_FOUND)

            except OperationalError:
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(0.1)
                    continue
                return Response(
                    {"error": "Database conflict. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def _approve_payment_request(self, payment_request, current_user):
        """
        Handles approval of a payment request.
        """
        if current_user == payment_request.requesting_user:
            return Response(
                {"error": "You are not authorized to approve this request."},
                status=status.HTTP_403_FORBIDDEN
            )

        if (payment_request.amount > TRANSFER_LIMIT
                and not payment_request.requested_user.is_verified):
            return Response(
                {"error": f"Verify your account to transfer more than {payment_request.currency} {TRANSFER_LIMIT}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        currency_obj = wallet_models.Currency.objects.get(code=payment_request.currency)
        requester_wallet = wallet_models.DigitalWallet.objects.select_for_update().get(
            wallet_owner=payment_request.requesting_user,
            currency=currency_obj.id
        )

        requestee_wallet, _ = wallet_models.DigitalWallet.objects.select_for_update().get_or_create(
            wallet_owner=payment_request.requested_user,
            currency=currency_obj.id 
        )

        transaction_charge = TransactionFeeCalculator.calculate_transaction_fees(payment_request.amount)
        if requestee_wallet.balance < (payment_request.amount + transaction_charge):
            return Response(
                {"error": "Insufficient balance in the requestee's wallet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        reference_id = ReferenceGenerator.payment_request_reference()

        requestee_wallet.balance -= (payment_request.amount + transaction_charge)
        requester_wallet.balance += payment_request.amount
        requestee_wallet.save()
        requester_wallet.save()

        transaction_record = TransactionRecord.objects.create(
            sender_wallet=requestee_wallet,
            receiver_wallet=requester_wallet,
            request_record=payment_request,
            transaction_type=TransactionType.INTERNAL_TRANSFER,
            amount=payment_request.amount,
            currency=payment_request.currency,
            reference_id=reference_id,
            transaction_charge=transaction_charge,
            status=TransactionStatus.SUCCESS,
            payment_provider=settings.APP_NAME,
        )

        payment_request.status = RequestStatus.SUCCESS
        payment_request.action = RequestAction.APPROVE
        payment_request.save()

        db_transaction.on_commit(lambda: notify_transaction_approval.delay(transaction_record.id))

        return Response(self.serializer_response_class(transaction_record).data, status=status.HTTP_201_CREATED)

    def _cancel_payment_request(self, payment_request, current_user):
        """
        Handles cancellation of a payment request.
        """
        if current_user == payment_request.requesting_user:
            payment_request.status = RequestStatus.CANCELLED
            payment_request.action = RequestAction.CANCEL
        elif current_user == payment_request.requested_user:
            payment_request.status = RequestStatus.DECLINED
            payment_request.action = RequestAction.DECLINE

        payment_request.save()

        db_transaction.on_commit(lambda: notify_transaction_cancellation.delay(payment_request.id))

        return Response(self.serializer_class(payment_request).data, status=status.HTTP_201_CREATED)
