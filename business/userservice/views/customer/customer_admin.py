# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

# Project-specific imports
from userservice.models import Customer
from userservice.serializers import CustomerAdminReviewSerializer, CustomerSerializer
from userservice.notifications import send_verification_email
from rbac.permissions import MethodPermission, register_permissions


@register_permissions
@extend_schema(tags=["User Services - KYC"])
class CustomerRecordsAdminView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = CustomerSerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'view_customer_records'

    @extend_schema(
        request=None,
        responses=CustomerSerializer(many=True),
        operation_id="List Customer Records",
        description="Retrieve a list of customer records for all users or a specific user."
    )
    def get(self, request, id=None, *args, **kwargs):
        customer_records = Customer.objects.filter(user=user).first()

        paginator = LimitOffsetPagination()
        paginated_customer_records = paginator.paginate_queryset(customer_records, request)

        user_data_map = {}
        for record in paginated_customer_records:
            user = record.user
            if user.id not in user_data_map:
                user_data_map[user.id] = {
                    'id': user.id,
                    'full_name': user.get_full_name(),
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'is_active': user.is_active,
                    'is_verified': user.is_verified,
                    'date_joined': user.date_joined,
                    'customer_records': []
                }
            user_data_map[user.id]['customer_records'].append(self.serializer_class(record).data)

        return paginator.get_paginated_response(list(user_data_map.values()))


@register_permissions
@extend_schema(tags=["User Services - KYC"])
class CustomerAdminUpdateView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = CustomerAdminReviewSerializer

    # Method-specific permissions for implemented methods only
    put_permission = 'update_customer_record'

    @extend_schema(
        request=serializer_class,
        responses={200: {"message": "Customer record updated successfully."}},
        operation_id="Verify Customer Record (Admin)",
        description="Admin endpoint to update customer records for users."
    )
    def put(self, request, id, *args, **kwargs):
        customer_record = get_object_or_404(Customer, id=id)
        serializer = self.serializer_class(customer_record, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                customer_record.refresh_from_db()
                user = customer_record.user
                user.is_verified = customer_record.customer_verified
                user.save()
                transaction.on_commit(lambda: send_verification_email.delay(
                    customer_record.id, verification_status=customer_record.verification_status
                ))
            return Response({"message": "Customer record updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
