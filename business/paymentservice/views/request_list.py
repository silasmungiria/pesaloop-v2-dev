# Third-party library imports
from django.db import models
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from paymentservice.models import RequestedTransaction
from paymentservice.serializers import RequestedTransactionSerializer


@register_permissions
@extend_schema(tags=["Payment Service - Request"])
class RequestListView(APIView):
    """
    Retrieves a list of payment requests for the authenticated user.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = RequestedTransactionSerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'list_payment_requests'

    @extend_schema(
        request=None,
        responses=RequestedTransactionSerializer(many=True),
        operation_id="List Payment Requests",
        description="Endpoint for retrieving payment requests where the authenticated user is either the requester or requestee."
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve payment requests involving the authenticated user.
        """
        payment_requests = RequestedTransaction.objects.filter(
            models.Q(requesting_user=request.user) | models.Q(requested_user=request.user)
        ).all()

        paginator = LimitOffsetPagination()
        paginated_requests = paginator.paginate_queryset(payment_requests, request)

        return paginator.get_paginated_response(self.serializer_class(paginated_requests, many=True).data)
