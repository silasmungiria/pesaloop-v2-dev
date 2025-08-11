from decimal import Decimal
from django.conf import settings
from django.db import transaction as db_transaction, DatabaseError
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from common import ReferenceGenerator
from rbac.permissions import MethodPermission, register_permissions
from walletservice import models as wallet_models
from forexservice.serializers import (
  ExchangeRequestSerializer,
  ExchangeExecutionResponseSerializer,
)
from forexservice.models import CurrencyExchangeRecord
from forexservice.services import ExchangeService
from forexservice.utils import ExchangeStatusChoices, CURRENCY_EXCHANGE_FEE
from forexservice.notifications import (
  dispatch_wallet_created_task,
  dispatch_exchange_success_task,
)


@register_permissions
@extend_schema(tags=["Forex Services - Execute Exchange"])
class ExchangeExecuteView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = ExchangeRequestSerializer
    response_serializer_class = ExchangeExecutionResponseSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'execute_currency_exchange'

    def _lock_src_wallet(self, user, currency_code):
        """Fetch and lock source wallet for update."""
        try:
            wallet = wallet_models.DigitalWallet.objects.select_for_update().filter(
                wallet_owner=user,
                currency__code=currency_code,
                is_active=True,
            ).first()
        except DatabaseError:
            return None, "Database error while fetching wallet."

        if not wallet:
            return None, "Wallet not found in this currency."
        return wallet, None

    def _validate_currency(self, currency_code):
        """Validate if target currency exists."""
        target = wallet_models.Currency.objects.filter(code=currency_code).first()
        if not target:
            return None, "Currency not supported."
        return target, None

    def _get_or_create_wallet(self, user, target_currency):
        """Get or create target wallet."""
        wallet, created = wallet_models.DigitalWallet.objects.get_or_create(
            wallet_owner=user,
            currency=target_currency,
            defaults={
                'is_default': False,
                'is_active': True,
                'balance': Decimal(0),
                'last_updated': timezone.now(),
            }
        )
        if created:
            db_transaction.on_commit(lambda: dispatch_wallet_created_task.delay(wallet.id, user.id))
        return wallet

    @extend_schema(
        request=serializer_class,
        responses=response_serializer_class,
        operation_id="Execute Currency Exchange",
        description="Execute the currency exchange transaction.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        src_code = serializer.validated_data['source_currency']
        tgt_code = serializer.validated_data['target_currency']
        amount = Decimal(serializer.validated_data['source_amount'])
        fee_pct = Decimal(CURRENCY_EXCHANGE_FEE)

        # Validate target currency before proceeding
        target_currency, error = self._validate_currency(tgt_code)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        # Perform conversion calculation
        try:
            base_rate, platform_rate, charged_fee, net_converted = ExchangeService.convert_amount(
                amount, src_code, tgt_code, fee_pct
            )
        except Exception as e:
            return Response({"error": f"Conversion failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        reference_id = ReferenceGenerator.forex_reference()

        try:
            with db_transaction.atomic():
                # Fetch and lock source wallet
                source_wallet, error = self._lock_src_wallet(request.user, src_code)
                if error:
                    return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

                # Check available balance
                if source_wallet.balance < amount:
                    return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

                # Adjust amount if balance would fall below 1 unit
                if source_wallet.balance - amount < 1:
                    amount = source_wallet.balance

                    # Recalculate conversion if amount changed
                    base_rate, platform_rate, charged_fee, net_converted = ExchangeService.convert_amount(
                        amount, src_code, tgt_code, fee_pct
                    )

                # Get or create target wallet
                target_wallet = self._get_or_create_wallet(request.user, target_currency)

                # Update wallet balances
                source_wallet.balance -= amount
                source_wallet.save()

                target_wallet.balance += net_converted
                target_wallet.save()

                # Create exchange record
                exchange_record = CurrencyExchangeRecord.objects.create(
                    user=request.user,
                    source_currency=src_code,
                    target_currency=tgt_code,
                    source_amount=amount,
                    base_exchange_rate=base_rate,
                    platform_exchange_rate=platform_rate,
                    charged_amount=charged_fee,
                    charged_amount_currency=src_code,
                    converted_amount_with_fee=net_converted,
                    reference_id=reference_id,
                    status=ExchangeStatusChoices.SUCCESS,
                    payment_provider=f'{settings.APP_NAME}',
                )

                # Notify after commit
                db_transaction.on_commit(lambda: dispatch_exchange_success_task.delay(
                    exchange_record.id, request.user.id
                ))

        except DatabaseError:
            return Response({"error": "Database operation failed. Please retry."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = self.response_serializer_class(
            source_currency=src_code,
            target_currency=tgt_code,
            source_amount=amount,
            base_exchange_rate=base_rate,
            platform_exchange_rate=platform_rate,
            charged_amount=charged_fee,
            converted_amount_with_fee=net_converted,
            reference_id=reference_id,
            status=exchange_record.status,
            payment_provider=f'{settings.APP_NAME}',
        )

        return Response(response_data.data, status=status.HTTP_200_OK)