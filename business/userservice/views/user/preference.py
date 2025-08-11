# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.serializers import NotificationPreferenceSerializer


@register_permissions
@extend_schema(tags=["User Services - User Management"])
class NotificationPreferenceView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = NotificationPreferenceSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'update_notification_preference'

    @extend_schema(
        request=serializer_class,
        responses={200: {"message": "Notification channel has been updated successfully."}},
        operation_id="Update Notification Preference",
        description="Endpoint for users to update their notification preferences."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.use_sms = serializer.validated_data['use_sms']
            user.save()
            return Response({"message": "Notification channel has been updated successfully.", "use_sms": user.use_sms})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
