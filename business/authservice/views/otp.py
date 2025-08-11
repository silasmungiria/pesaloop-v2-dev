import logging

# Django/DRF imports
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Project imports
from userservice.models import User
from authservice.serializers import (
    RegisterVerificationSerializer,
    ResendOTPSerializer
)
from authservice.services import OTPManager
from authservice.notifications import (
    dispatch_sms_verification_otp_task,
    dispatch_email_verification_otp_task
)
from tracking.services import track_activity
from tracking.utils import ActivityType


logger = logging.getLogger(__name__)


def get_user_by_identifier(identifier: str):
    """Fetch user by email or phone identifier."""
    user = User.objects.filter(
        Q(email=identifier.lower()) | Q(phone_number=identifier)
    ).first()

    if not user:
        logger.warning("User lookup failed for identifier: %s", identifier)
        return None

    return user


def build_verification_status(user: User) -> dict:
    """Construct verification status response."""
    return {
        "account_verified": user.is_active,
        "is_email_verified": user.verified_email,
        "is_phone_verified": user.verified_phone_number,
    }


@extend_schema(tags=["Authentication - TOTP Verification"])
class ActivateAccountWithOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterVerificationSerializer

    @extend_schema(
        request=RegisterVerificationSerializer,
        responses={200: {"description": "Account activated successfully."}},
        operation_id="Activate Account with TOTP",
        description="Activate user account using TOTP verification."
    )
    @track_activity(activity_type=ActivityType.AUTH, async_mode=True, sensitive_fields=['otp'])
    def post(self, request):
        logger.info("Received TOTP verification request.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid TOTP verification data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        identifier = serializer.validated_data["identifier"]
        otp = serializer.validated_data["otp"]

        user = get_user_by_identifier(identifier)
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if not OTPManager.validate_otp(user.id, otp):
            logger.warning("Invalid TOTP for user %s", user.id)
            return Response({"error": "Invalid TOTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Update verification status
        if user.email == identifier.lower():
            user.verified_email = True
            logger.info("Email verified for user %s", user.id)
        if user.phone_number == identifier:
            user.verified_phone_number = True
            logger.info("Phone number verified for user %s", user.id)

        user.is_active = user.verified_email and user.verified_phone_number
        user.save()
        user.refresh_from_db()

        user_verified = build_verification_status(user)
        new_otp = OTPManager.generate_otp(user.id)

        # Dispatch next TOTP if needed
        if user.verified_email and not user.verified_phone_number:
            dispatch_sms_verification_otp_task.delay(new_otp, user.phone_number)
            logger.info("Dispatched SMS TOTP for phone verification to user %s", user.id)
            return Response({
                "message": "Email verified. Verify phone number to complete registration.",
                "user_verified": user_verified
            }, status=status.HTTP_200_OK)

        if user.verified_phone_number and not user.verified_email:
            dispatch_email_verification_otp_task.delay(new_otp, user.email)
            logger.info("Dispatched email TOTP for email verification to user %s", user.id)
            return Response({
                "message": "Phone number verified. Verify email to complete registration.",
                "user_verified": user_verified
            }, status=status.HTTP_200_OK)

        logger.info("Account verification complete for user %s", user.id)
        return Response({
            "message": "Account verification complete.",
            "user_verified": user_verified
        }, status=status.HTTP_200_OK)



@extend_schema(tags=["Authentication - TOTP Verification"])
class ResendOTPVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendOTPSerializer

    @extend_schema(
        request=ResendOTPSerializer,
        responses={200: {"description": "OTP sent successfully."}},
        operation_id="Resend TOTP Verification",
        description="Resend TOTP for account activation."
    )
    @track_activity(activity_type=ActivityType.AUTH, async_mode=True, sensitive_fields=['otp'])
    def post(self, request):
        logger.info("Received resend TOTP request.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid resend TOTP request: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        identifier = serializer.validated_data["identifier"]
        user = get_user_by_identifier(identifier)

        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp = OTPManager.generate_otp(user.id)

        if user.verified_email and not user.verified_phone_number:
            dispatch_sms_verification_otp_task.delay(otp, user.phone_number)
            logger.info("Resent TOTP via SMS to user %s", user.id)

        elif user.verified_phone_number and not user.verified_email:
            dispatch_email_verification_otp_task.delay(otp, user.email)
            logger.info("Resent TOTP via email to user %s", user.id)

        else:
            dispatch_email_verification_otp_task.delay(otp, user.email)
            logger.info("Resent TOTP via default channel (email) to user %s", user.id)

        return Response(
            {"message": "TOTP has been sent successfully."},
            status=status.HTTP_200_OK
        )
