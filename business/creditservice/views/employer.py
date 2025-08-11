from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from creditservice.models import Employer
from creditservice.serializers import (
    EmployerSerializer,
    EmployerRegistrationSerializer,
    EmployerVerificationSerializer
)
from creditservice.services.verification import VerificationService
from rbac.permissions import MethodPermission, register_permissions


@register_permissions
@extend_schema(tags=['Credit Service - Employer'])
class EmployerRegistrationAPIView(APIView):
    permission_classes = []
    serializer_class = EmployerRegistrationSerializer
    response_serializer_class = EmployerSerializer

    post_permission = 'register_credit_employer'

    @extend_schema(
        request=serializer_class,
        responses={status.HTTP_201_CREATED: response_serializer_class},
        operation_id='Register Credit Employer',
        description='Register a new employer and create an account.'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        employer = serializer.save()

        return Response(
            self.response_serializer_class(employer).data,
            status=status.HTTP_201_CREATED
        )


@register_permissions
@extend_schema(tags=['Credit Service - Employer'])
class EmployerVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = EmployerVerificationSerializer
    response_serializer_class = EmployerSerializer

    post_permission = 'verify_credit_employer'

    @extend_schema(
        request=serializer_class,
        responses={status.HTTP_200_OK: response_serializer_class},
        operation_id='Verify Credit Employer',
        description='Verify an employer account by an authorized user.'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        employer_id = serializer.validated_data['employer_id']

        try:
            employer = Employer.objects.select_for_update().get(id=employer_id)
        except Employer.DoesNotExist:
            return Response(
                {"error": "Employer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            VerificationService.verify_employer(employer, request.user)
            return Response(
                self.response_serializer_class(employer).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
