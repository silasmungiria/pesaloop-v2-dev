# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.serializers import ChangeEmailSerializer


@register_permissions
@extend_schema(tags=["User Services - User Management"])
class ChangeEmailView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = ChangeEmailSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'change_email'

    @extend_schema(
        request=serializer_class,
        responses=None,
        operation_id="Change User Email",
        description="Endpoint for users to change their email address."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['currentPassword']):
                return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.email = serializer.validated_data['email']
            user.save()
            return Response({"message": "Email has been changed successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
