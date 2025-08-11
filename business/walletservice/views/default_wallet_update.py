# Third-party library imports
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from walletservice.models import DigitalWallet
from walletservice.serializers import WalletSerializer, SetDefaultWalletSerializer


@register_permissions
@extend_schema(tags=["Wallet Services - Wallets"])
class SetDefaultWalletView(APIView):
    """
    Set the default wallet for the authenticated user.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class =  SetDefaultWalletSerializer

    # Method-specific permissions for implemented methods only
    put_permission = 'set_default_wallet'

    def get_object(self, id):
        """
        Retrieve the wallet object for the given ID and authenticated user.
        """
        try:
            return DigitalWallet.objects.get(id=id, wallet_owner=self.request.user)
        except DigitalWallet.DoesNotExist:
            return None

    @extend_schema(
        request=SetDefaultWalletSerializer,
        responses=WalletSerializer,
        operation_id="Set Default Wallet",
        description="Set the default wallet for the authenticated user."
    )
    def put(self, request, id):
        """
        Set the default wallet for the authenticated user.
        """
        wallet = self.get_object(id)
        is_default = request.data.get('is_default')

        if is_default is None:
            return Response({"error": "is_default field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not wallet:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        if wallet.is_default:
            return Response({"error": "Cannot unset a default wallet."}, status=status.HTTP_400_BAD_REQUEST)

        if wallet.is_default and not is_default:
            return Response({"error": "Cannot set wallet as default unless specified."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            DigitalWallet.objects.filter(wallet_owner=request.user).update(is_default=False)
            wallet.is_default = serializer.validated_data.get('is_default', wallet.is_default)
            wallet.save()
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
