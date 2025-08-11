import logging

# Django/DRF imports
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Project-specific imports
from userservice.models import User
from authservice.serializers import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)
from authservice.services import token_generator
from authservice.notifications import (
    dispatch_password_reset_email_task,
    dispatch_password_reset_confirmation_email_task
)
from tracking.services import track_activity
from tracking.utils import ActivityType


logger = logging.getLogger(__name__)

@extend_schema(tags=["Authentication - Password Reset"])
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: {"description": "Password reset link sent successfully."}},
        operation_id="Forgot Password",
        description="Initiate password reset by sending a reset link to the user's email."
    )
    @track_activity(activity_type=ActivityType.AUTH, async_mode=True, sensitive_fields=['email'])
    def post(self, request):
        logger.info("Received forgot password request.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid forgot password request data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        identifier = serializer.validated_data["identifier"]
        user = User.objects.filter(email=identifier.lower()).first()

        if not user:
            logger.warning("Forgot password failed: No user found with email %s", identifier)
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        dispatch_password_reset_email_task.delay(user.id)
        logger.info("Dispatched password reset email for user %s", user.id)

        return Response(
            {"message": "Password reset link sent successfully."},
            status=status.HTTP_200_OK
        )



@extend_schema(tags=["Authentication - Password Reset"])
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: {"description": "Password reset successful."}},
        operation_id="Reset Password",
        description="Reset user password using the provided token and UID."
    )
    @track_activity(activity_type=ActivityType.AUTH, async_mode=True, sensitive_fields=['new_password'])
    def post(self, request):
        logger.info("Received password reset request.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid reset password data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            logger.debug("Decoded UID %s to user ID %s", uid, user_id)

            if not token_generator.check_token(user, token):
                logger.warning("Invalid or expired token for user %s", user_id)
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.password_reset_count += 1
            user.last_password_reset = timezone.now()
            user.save()

            dispatch_password_reset_confirmation_email_task.delay(user.id)
            logger.info("Password reset successful for user %s", user.id)

            return Response(
                {"message": "Password reset successful. You can now log in with your new password."},
                status=status.HTTP_200_OK
            )

        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as e:
            logger.error("Failed to reset password with UID %s: %s", uid, str(e))
            return Response({"error": "Invalid UID or token."}, status=status.HTTP_400_BAD_REQUEST)
