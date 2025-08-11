# Standard library imports
from uuid import UUID

# Third-party library imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from walletservice.models import Currency
from walletservice.serializers import CurrencySerializer


@register_permissions
@extend_schema(tags=["Wallet Services - Currencies"])
class CurrencyDetailView(APIView):
    """
    Retrieve, update, or delete a currency by its ID.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = CurrencySerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'view_currency'
    put_permission = 'change_currency'
    delete_permission = 'delete_currency'

    def get_object(self, id):
        """
        Retrieve a currency object by its ID.
        """
        try:
            if isinstance(id, str):
                id = UUID(id)
            return Currency.objects.get(id=id)
        except (Currency.DoesNotExist, ValueError):
            return None

    @extend_schema(
        request=None,
        responses=CurrencySerializer,
        operation_id="Retrieve Currency by ID",
        description="Retrieve a currency by its ID."
    )
    def get(self, request, id):
        """
        Retrieve a currency by its ID.
        """
        currency = self.get_object(id)
        if currency:
            serializer = CurrencySerializer(currency)
            return Response(serializer.data)
        return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=CurrencySerializer,
        responses=CurrencySerializer,
        operation_id="Update Currency by ID",
        description="Update a currency by its ID."
    )
    def put(self, request, id):
        """
        Update a currency by its ID.
        """
        currency = self.get_object(id)
        if currency:
            serializer = CurrencySerializer(currency, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=None,
        responses=None,
        operation_id="Delete Currency by ID",
        description="Delete a currency by its ID."
    )
    def delete(self, request, id):
        """
        Delete a currency by its ID.
        """
        currency = self.get_object(id)
        if currency:
            currency.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)
