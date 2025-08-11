# Third-party library imports
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Project-specific imports
from ..models import DigitalWallet
from ..serializers import DevelopmentWalletTopUpSerializer


class DevelopmentWalletTopUpView(APIView):
    """
    Top up the development wallet for testing purposes.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DevelopmentWalletTopUpSerializer

    @extend_schema(request=DevelopmentWalletTopUpSerializer, responses=None)
    def post(self, request):
        """
        Top up the development wallet for testing purposes.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get('amount')
            currency = serializer.validated_data.get('currency')
            wallet_owner = serializer.validated_data.get('wallet_owner')

            wallet = DigitalWallet.objects.filter(wallet_owner=wallet_owner, currency=currency).first()
            if wallet:
                wallet.balance += amount
                wallet.save()
                return Response({"message": "Wallet topped up successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)