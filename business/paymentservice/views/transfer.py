# Standard library imports
import time
from decimal import Decimal

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
from paymentservice.models import TransactionRecord
from paymentservice.serializers import (
    InitiateP2PTransferSerializer,
    TransactionRecordSerializer
)
from paymentservice.services import TransactionFeeCalculator
from paymentservice.utils import TransferLimits, TransactionStatus,  TransactionType
from paymentservice.notifications import notify_transaction_completion


TRANSFER_LIMIT = TransferLimits.UNVERIFIED_WALLET_MAX_TRANSFER


@register_permissions
@extend_schema(tags=["Payment Service - Records"])
class TransferCreateView(APIView):
    """
    Handles peer-to-peer (P2P) wallet transfers between users.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = InitiateP2PTransferSerializer
    serializer_response_class = TransactionRecordSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'create_p2p_transfer'

    @extend_schema(
        request=InitiateP2PTransferSerializer,
        responses=TransactionRecordSerializer,
        operation_id="Create P2P Transfer",
        description="Endpoint for processing a peer-to-peer transfer from one user's wallet to another user's wallet."
    )
    def post(self, request, *args, **kwargs):
        """
        Sends funds from one user's wallet to another user's wallet.
        """
        MAX_RETRIES = 3

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sender_user_id = request.user.id
        recipient_user_id = serializer.validated_data['recipient_user']
        transfer_amount = serializer.validated_data['transfer_amount']
        reason = serializer.validated_data.get('reason', None)

        try:
            transfer_amount = Decimal(transfer_amount)
            if transfer_amount <= 0:
                return Response({"error": "Amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({"error": "Invalid transfer amount."}, status=status.HTTP_400_BAD_REQUEST)

        if sender_user_id == recipient_user_id:
            return Response({"error": "You cannot transfer funds to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        transaction_charge = TransactionFeeCalculator.calculate_transaction_fees(transfer_amount)

        try:
            sender_wallet = wallet_models.DigitalWallet.objects.get(wallet_owner=sender_user_id, is_default=True)
        except wallet_models.DigitalWallet.DoesNotExist:
            return Response({"error": "Sender wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        if transfer_amount > TRANSFER_LIMIT and not sender_wallet.wallet_owner.is_verified:
            return Response(
                {"error": f"Verify your account to transfer more than {sender_wallet.currency.code} {TRANSFER_LIMIT}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if sender_wallet.balance < transfer_amount + transaction_charge:
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        receiver_wallet, _ = wallet_models.DigitalWallet.objects.get_or_create(
            wallet_owner_id=recipient_user_id,
            currency=sender_wallet.currency,
            defaults={'is_default': False, 'balance': Decimal(0.00)},
        )

        for attempt in range(MAX_RETRIES):
            try:
                with db_transaction.atomic():
                    reference_id = ReferenceGenerator.transaction_reference()

                    sender_wallet.balance -= (transfer_amount + transaction_charge)
                    receiver_wallet.balance += transfer_amount
                    sender_wallet.save()
                    receiver_wallet.save()

                    transaction_record = TransactionRecord.objects.create(
                        sender_wallet=sender_wallet,
                        receiver_wallet=receiver_wallet,
                        transaction_type=TransactionType.INTERNAL_TRANSFER,
                        amount=transfer_amount,
                        currency=sender_wallet.currency.code,
                        reference_id=reference_id,
                        transaction_charge=transaction_charge,
                        status=TransactionStatus.SUCCESS,
                        payment_provider=settings.APP_NAME,
                        reason=reason,
                    )

                db_transaction.on_commit(lambda: notify_transaction_completion.delay(transaction_record.id))

                return Response(self.serializer_response_class(transaction_record).data, status=status.HTTP_201_CREATED)

            except OperationalError:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(0.1)
                    continue
                return Response({"error": "Database conflict, please retry the operation."}, status=status.HTTP_409_CONFLICT)

            except Exception as e:
                return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
