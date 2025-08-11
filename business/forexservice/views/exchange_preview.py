from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from rbac.permissions import MethodPermission, register_permissions
from forexservice.serializers import ExchangeRequestSerializer, ExchangePreviewResponseSerializer
from forexservice.services import ExchangeService
from forexservice.utils import CURRENCY_EXCHANGE_FEE


@register_permissions
@extend_schema(tags=["Forex Services - Preview Exchange"])
class ExchangePreviewView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = ExchangeRequestSerializer
    response_serializer_class = ExchangePreviewResponseSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'preview_currency_exchange'

    @extend_schema(
            request=serializer_class,
            responses=response_serializer_class,
            operation_id="Preview Currency Exchange",
            description="Preview the currency exchange details before confirming the transaction.",
            )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            src_currency = serializer.validated_data['source_currency']
            tgt_currency = serializer.validated_data['target_currency']
            amount = Decimal(serializer.validated_data['source_amount'])

            try:
                res = ExchangeService.convert_amount(
                    amount, src_currency, tgt_currency, fee_percentage=Decimal(CURRENCY_EXCHANGE_FEE)
                )
                response_data = self.response_serializer_class(data={
                    "source_currency": src_currency,
                    "target_currency": tgt_currency,
                    "source_amount": amount,
                    "platform_exchange_rate": res[1],
                    "charged_amount": res[2],
                    "converted_amount_with_fee": res[3],
                })
                
                if response_data.is_valid():
                    return Response(response_data.data, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)