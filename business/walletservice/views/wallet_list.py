# Third-party library imports
from aiohttp import request
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

# Project-specific imports
from walletservice.models import DigitalWallet
from walletservice.serializers import WalletSerializer
from rbac.permissions import MethodPermission, register_permissions


@register_permissions
@extend_schema(tags=["Wallet Services - Wallets"])
class ListWalletsView(APIView):
    """
    List all wallets for the authenticated user.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = WalletSerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'view_wallets'

    @extend_schema(
        request=None,
        responses=WalletSerializer(many=True),
        operation_id="List All Wallets",
        description="Retrieve a list of all wallets for the authenticated user."
    )
    def get(self, request):
        """
        List all available wallets for the authenticated user.
        """
        try:
            wallets = DigitalWallet.objects.filter(wallet_owner=request.user).select_related('currency').order_by('-created_at')

            paginator = LimitOffsetPagination()
            paginated_wallets = paginator.paginate_queryset(wallets, request)
            serializer = WalletSerializer(paginated_wallets, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
