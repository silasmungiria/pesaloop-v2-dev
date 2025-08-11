# Third-party library imports
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from walletservice.models import DigitalWallet
from walletservice.serializers import WalletActivateSerializer, WalletSerializer


@register_permissions
@extend_schema(tags=["Wallet Services - Wallets"])
class ActivateWalletView(APIView):
    """
    Activate a wallet for the authenticated user.
    """
    serializer_class = WalletActivateSerializer
    permission_classes = [IsAuthenticated, MethodPermission]

    # Method-specific permissions for implemented methods only
    put_permission = 'activate_wallet'

    def get_object(self, id):
        """
        Retrieve a wallet object by its ID.
        """
        try:
            return DigitalWallet.objects.get(id=id)
        except DigitalWallet.DoesNotExist:
            return None

    @extend_schema(
        request=WalletActivateSerializer,
        responses=WalletSerializer,
        operation_id="Activate Wallet",
        description="Activate a wallet by setting its 'is_active' status to True."
    )
    def put(self, request, id):
        """
        Activate the wallet by setting its 'is_active' status to False.
        """
        wallet = self.get_object(id)
        is_active = request.data.get('is_active')

        if is_active is None:
            return Response({"error": "is_active field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_active == True:
            return Response({"error": "Wallet is not activated."}, status=status.HTTP_400_BAD_REQUEST)

        if not wallet:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if wallet.is_active == True:
            return Response({"error": "Wallet is already activated."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            wallet.is_active = True
            wallet.save()
            return Response({"message": "Wallet activated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
