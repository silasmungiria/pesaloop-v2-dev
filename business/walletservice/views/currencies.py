# Third-party library imports
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from walletservice.models import Currency
from walletservice.serializers import CurrencySerializer


@register_permissions
@extend_schema(tags=["Wallet Services - Currencies"])
class CurrencyView(APIView):
    """
    List all currencies and create a new currency.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = CurrencySerializer

    # Method-specific permissions
    get_permission = 'view_currency'
    post_permission = 'add_currency'

    @extend_schema(
        request=None,
        responses=CurrencySerializer(many=True),
        operation_id="List All Currencies",
        description="Retrieve a list of all available currencies."
    )
    def get(self, request):
        """
        List all available currencies.
        """
        try:
            currencies = Currency.objects.all().order_by('code')
            
            paginator = LimitOffsetPagination()
            paginated_currencies = paginator.paginate_queryset(currencies, request)
            serializer = CurrencySerializer(paginated_currencies, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=CurrencySerializer,
        responses=CurrencySerializer,
        operation_id="Create Currency",
        description="Create a new currency with the provided details."
    )
    def post(self, request):
        """
        Create a new currency.
        """
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
