# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.serializers import ChangePhoneNumberSerializer


@register_permissions
@extend_schema(tags=["User Services - User Management"])
class ChangePhoneNumberView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = ChangePhoneNumberSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'change_phone_number'

    @extend_schema(
        request=serializer_class,
        responses=None,
        operation_id="Change User Phone Number",
        description="Endpoint for users to change their phone number."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['currentPassword']):
                return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.phone_number = serializer.validated_data['phoneNumber']
            user.save()
            return Response({"message": "Phone number has been changed successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
