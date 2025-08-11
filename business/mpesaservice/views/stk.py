import base64
import logging
from decimal import Decimal
from datetime import datetime

from aiohttp import ClientSession, BasicAuth
from asgiref.sync import async_to_sync
from django.conf import settings
from django.db import transaction as db_transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common import ReferenceGenerator
from walletservice import models as wallet_models
from paymentservice import models as payments_models
from mpesaservice.serializers import TopUpRequestSerializer, TopUpResponseSerializer
from mpesaservice.services import JWTUtils
from mpesaservice.notifications import dispatch_wallet_top_up_initiated

logger = logging.getLogger(__name__)

@extend_schema(tags=["Integration - Mpesa STK"])
class STKPushView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopUpRequestSerializer

            
    # Get access token
    # def _get_access_token(self):
    #     consumer_key = "YchGcEDng1THuOJMy8dsjTdGyTVxG2zbepG4NlMpKNZ2owix"
    #     consumer_secret = "29Y9rSBfO4iuZCq0MCkOGZ3sowK1WhYeATcpGJHO6YmfZFiMIaDKABMu3DEZuEhs"
    #     endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    #     response = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    #     data = response.json()
    #     return data['access_token']

    async def _get_access_token(self):
        try:
            async with ClientSession() as session:
                endpoint = settings.MPESA_TOKEN_ENDPOINT
                consumer_key = settings.MPESA_CONSUMER_KEY
                consumer_secret = settings.MPESA_CONSUMER_SECRET
                auth = BasicAuth(consumer_key, consumer_secret)

                async with session.get(endpoint, auth=auth) as response:
                    data = await response.json()
                    logger.info(f"Access token response: {data}")
                    return data['access_token']
        except Exception as e:
            logger.error(f"Failed to get MPESA access token: {str(e)}")
            raise

    async def _process_payment(self, user_wallet, phone_number, topup_amount, reference_id, reason):
        try:
            access_token = await self._get_access_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            raw_password = f"{settings.MPESA_BUSINESS_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
            password = base64.b64encode(raw_password.encode('utf-8')).decode('utf-8')

            token = JWTUtils.encode_ref(reference_id)
            callback_url = f"{settings.MPESA_CALLBACK_URL}/?token={token}"

            payment_data = {
                "BusinessShortCode": settings.MPESA_BUSINESS_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": settings.MPESA_TRANSACTION_TYPE,
                "Amount": str(topup_amount),
                "PartyA": str(phone_number),
                "PartyB": settings.MPESA_PARTY_B_SHORTCODE,
                "PhoneNumber": phone_number,
                "CallBackURL": callback_url,
                "AccountReference": str(user_wallet.id),
                "TransactionDesc": reason or "Wallet Top-Up"
            }

            logger.info(f"STK Push request data: {payment_data}")

            async with ClientSession() as session:
                async with session.post(
                    settings.MPESA_STK_PUSH_ENDPOINT,
                    json=payment_data,
                    headers=headers
                ) as response:
                    resp = await response.json()
                    logger.info(f"STK Push response: {resp}")
                    return resp
        except Exception as e:
            logger.error(f"STK push request failed: {str(e)}")
            raise

    @extend_schema(
        request=TopUpRequestSerializer,
        responses=TopUpResponseSerializer,
        operation_id="STK Push Init",
        description="Endpoint for initiating a wallet top-up via MPESA STK Push."
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        logger.info(f"Top-up request data: {data}")

        try:
            topup_amount = Decimal(data.get('amount', '0'))
            phone_number = ''.join(filter(str.isdigit, data.get('phone_number', ''))).replace('+', '')
            reason = data.get('reason', 'Wallet Top-Up')

            if len(phone_number) != 12 or not phone_number.startswith('254'):
                return Response({"error": "Invalid phone number format."}, status=status.HTTP_400_BAD_REQUEST)

            if topup_amount <= 0:
                return Response({"error": "Invalid top-up amount."}, status=status.HTTP_400_BAD_REQUEST)

            reference_id = ReferenceGenerator.mpesa_reference()

            currency, _ = wallet_models.Currency.objects.get_or_create(code='KES', defaults={'name': 'Kenyan Shilling'})
            user_wallet, _ = wallet_models.DigitalWallet.objects.get_or_create(
                wallet_owner=user,
                currency=currency,
                defaults={'is_default': False, 'is_active': True}
            )

            with db_transaction.atomic():
                transaction_record = payments_models.TransactionRecord.objects.create(
                    sender_wallet=user_wallet,
                    receiver_wallet=user_wallet,
                    reference_id=reference_id,
                    transaction_type='TOPUP',
                    status='PENDING',
                    reason=reason,
                    payment_provider='MPESA',
                )
                transaction_record.amount = topup_amount
                transaction_record.save()

            payment_response = async_to_sync(self._process_payment)(
                user_wallet, phone_number, topup_amount, reference_id, reason
            )

            if payment_response.get("ResponseCode") == "0":
                with db_transaction.atomic():
                    transaction_record.status = 'MPESA_PENDING'
                    transaction_record.save()
                    db_transaction.on_commit(lambda: dispatch_wallet_top_up_initiated.delay(reference_id, phone_number))

                return Response(
                    {"message": "Payment initiated successfully.", "reference_id": reference_id},
                    status=status.HTTP_201_CREATED
                )
            else:
                transaction_record.status = 'FAILED'
                transaction_record.save()
                return Response({"error": payment_response.get("errorMessage", "Payment initiation failed.")},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Exception during STK Push")
            return Response(
                {"error": "An error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
