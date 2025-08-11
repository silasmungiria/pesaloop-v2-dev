# Standard library imports
import jwt
from decimal import Decimal

# Thrid party imports
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from drf_spectacular.utils import extend_schema

# Project-specific imports
from mpesaservice.services import JWTUtils
from mpesaservice.notifications import dispatch_wallet_top_up_confirmation
from paymentservice.models import TransactionRecord
from walletservice.models import DigitalWallet



@extend_schema(tags=["Integration - Mpesa STK"])
class STKCallbackView(APIView):
    """
    Handles the payment service callback to update transaction status.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses=None,
        operation_id="STK Push Callback",
        description="Endpoint for handling STK Push payment callbacks from Safaricom."
    )
    def post(self, request, *args, **kwargs):
        try:
            token = request.query_params.get('token')
            if not token:
                return Response({"error": "Missing token"}, status=400)

            try:
                payload = JWTUtils.decode_token(token)
                reference_id = payload.get('ref')
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token expired"}, status=400)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=400)

            callback_data = request.data
            stk_callback = callback_data.get('Body', {}).get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')

            transaction = TransactionRecord.objects.filter(reference_id=reference_id).first()
            if not transaction:
                return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

            if result_code == 0:
                callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                metadata = {}

                for item in callback_metadata:
                    # Save all callback data in metadata except Amount
                    metadata[item.get('Name')] = item.get('Value')
                    if item.get('Name') == 'Amount':
                        transaction.amount = Decimal(item.get('Value'))

                # Save the entire callback data in metadata as JSON
                transaction.metadata = callback_data

                transaction.status = 'SUCCESS'
                transaction.receiver_wallet.balance += transaction.amount
                transaction.receiver_wallet.save()
                transaction.save()

                # Notify only after transaction is committed
                db_transaction.on_commit(lambda: dispatch_wallet_top_up_confirmation.delay(reference_id))

                return Response({"message": "Transaction successful"}, status=status.HTTP_200_OK)

            elif result_code == 1032:
                transaction.status = 'CANCELLED'
                transaction.metadata = callback_data
                transaction.save()
                return Response({"message": "Payment cancelled"}, status=status.HTTP_200_OK)

            else:
                transaction.status = 'FAILED'
                transaction.metadata = callback_data
                transaction.save()
                return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=["Integration - Mpesa C2B"])
class C2BCallbackView(APIView):
    """
    Handles direct Paybill C2B payment confirmation callbacks from Safaricom.

    Expected callback payload:
    ```json
    {
        "TransactionType": "Pay Bill",
        "TransID": "RKTQDM7W6S",
        "TransTime": "20191122063845",
        "TransAmount": "10",
        "BusinessShortCode": "600638",
        "BillRefNumber": "invoice008",
        "InvoiceNumber": "",
        "OrgAccountBalance": "",
        "ThirdPartyTransID": "",
        "MSISDN": "25470****149",
        "FirstName": "John",
        "MiddleName": "",
        "LastName": "Doe"
    }
    ```
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses=None,
        operation_id="C2B Confirm Callback",
        description="Endpoint for handling C2B Paybill payment confirmation callbacks from Safaricom."
    )
    def post(self, request, *args, **kwargs):
        callback_data = request.data

        try:
            # Extract required fields
            trans_id = callback_data.get("TransID")
            trans_amount = callback_data.get("TransAmount")
            bill_ref_number = callback_data.get("BillRefNumber")

            if not all([trans_id, trans_amount, bill_ref_number]):
                return Response(
                    {"ResultCode": 1, "ResultDesc": "Missing required transaction fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Map BillRefNumber to wallet (here you assume bill_ref_number is wallet.id)
            wallet = DigitalWallet.objects.filter(id=bill_ref_number).first()
            if not wallet:
                # Per Safaricom docs, always respond with 200 and ResultCode 0 even if you don't process it
                return Response(
                    {"ResultCode": 0, "ResultDesc": "Wallet not found"},
                    status=status.HTTP_200_OK
                )

            # Create transaction record
            TransactionRecord.objects.create(
                sender_wallet=wallet,
                receiver_wallet=wallet,
                reference_id=trans_id,
                amount=Decimal(trans_amount),
                transaction_type='PAYBILL_TOPUP',
                status='SUCCESS',
                reason='C2B Paybill Top-Up',
                payment_provider='MPESA',
                metadata=callback_data  # store full callback payload for auditing
            )

            # Update wallet balance
            wallet.balance += Decimal(trans_amount)
            wallet.save()

            # Successful acknowledgment to Safaricom
            return Response({"ResultCode": 0, "ResultDesc": "Accepted"}, status=status.HTTP_200_OK)

        except Exception:
            # Return a 500 but still a Safaricom-valid result structure
            return Response(
                {"ResultCode": 1, "ResultDesc": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

