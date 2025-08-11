### C:\Users\mungi\Projects\sendpesa\business\userservice\views\merchant\registration.py ###
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from drf_spectacular.utils import extend_schema

from rbac.permissions import MethodPermission, register_permissions
from rbac.models import Role, UserRole
from userservice.models import Merchant
from userservice.serializers import UserProfileStandardSerializer, MerchantSerializer


@register_permissions
@extend_schema(tags=["User Services - Merchant"])
class MerchantRegistrationAPIView(APIView):
    """
    Register a new merchant
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = MerchantSerializer
    serializer_class_user = UserProfileStandardSerializer

    post_permission = 'register_merchant'

    @extend_schema(
        request=serializer_class,
        responses={201: {"message": "Merchant registration successful. Account will be activated after verification."}},
        operation_id="Register Merchant",
        description="Endpoint for merchants to register their business and user profile."
    )
    def post(self, request):
        user_serializer = self.serializer_class_user(data=request.data)
        merchant_serializer = self.serializer_class(data=request.data)
        
        # Validate both serializers first
        user_valid = user_serializer.is_valid()
        merchant_valid = merchant_serializer.is_valid()
        
        if not (user_valid and merchant_valid):
            errors = {}
            if not user_valid:
                errors.update({'user_errors': user_serializer.errors})
            if not merchant_valid:
                errors.update({'merchant_errors': merchant_serializer.errors})
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Create user but don't activate yet
                user_data = user_serializer.validated_data.copy()
                user_data['is_active'] = False  # Don't activate immediately
                user = self.serializer_class_user.Meta.model.objects.create_user(**user_data)

                # Assign merchant role
                merchant_role, _ = Role.objects.get_or_create(name='merchant')
                UserRole.objects.create(user=user, role=merchant_role)

                # Create merchant profile
                merchant_data = merchant_serializer.validated_data
                Merchant.objects.create(user=user, **merchant_data)

                return Response(
                    {'message': 'Merchant registration successful. Account will be activated after verification.'},
                    status=status.HTTP_201_CREATED
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
