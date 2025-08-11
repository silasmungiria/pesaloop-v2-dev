from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from creditservice.models import CreditUser
from creditservice.serializers import (
    CreditUserSerializer,
    EmployeeRegistrationSerializer,
    UserVerificationInputSerializer
)
from creditservice.services.verification import VerificationService
from rbac.permissions import MethodPermission, register_permissions


@register_permissions
@extend_schema(tags=['Credit Service - Employee'])
class UserVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = UserVerificationInputSerializer
    response_serializer_class = CreditUserSerializer
    post_permission = 'verify_credit_user'

    @extend_schema(
        request=serializer_class,
        responses={status.HTTP_200_OK: response_serializer_class},
        operation_id='Verify Credit User',
        description='Verify a credit user by employer admin.'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        try:
            credit_user = CreditUser.objects.select_for_update().get(user_id=validated['user_id'])
        except CreditUser.DoesNotExist:
            raise NotFound("User not found")

        credit_user.monthly_salary = validated['monthly_salary']
        VerificationService.verify_employee(credit_user, request.user)

        return Response(
            self.response_serializer_class(credit_user).data,
            status=status.HTTP_200_OK
        )


@register_permissions
@extend_schema(tags=['Credit Service - Employee'])
class EmployeeRegistrationAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = EmployeeRegistrationSerializer
    response_serializer_class = CreditUserSerializer
    post_permission = 'register_credit_employee'

    @extend_schema(
        request=serializer_class,
        responses={status.HTTP_201_CREATED: response_serializer_class},
        operation_id='Register Credit Employee',
        description='Register an employee and associate with employer.'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()

        return Response(
            self.response_serializer_class(employee).data,
            status=status.HTTP_201_CREATED
        )


@register_permissions
@extend_schema(tags=['Credit Service - Employee'])
class UserProfileAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = CreditUserSerializer
    get_permission = 'view_credit_user_profile'

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class},
        operation_id='Retrieve Credit User Profile',
        description='Get authenticated user\'s credit profile.'
    )
    def get(self, request, *args, **kwargs):
        try:
            credit_user = request.user.credit_profile
        except CreditUser.DoesNotExist:
            raise NotFound("Credit profile not found.")

        return Response(
            self.serializer_class(credit_user).data,
            status=status.HTTP_200_OK
        )
