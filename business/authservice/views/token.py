import logging

# Django & DRF imports
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Project imports
from userservice.models import User
from userservice.services import CustomerProfileFormatter
from authservice.serializers import (
    CreateJWTSerializer,
    RefreshTokenSerializer,
    RevokeTokenSerializer,
)
from authservice.services import OTPManager
from authservice.notifications import (
    dispatch_sms_verification_otp_task,
    dispatch_email_verification_otp_task,
)
from tracking.services import track_activity
from tracking.utils import ActivityType

logger = logging.getLogger(__name__)


@extend_schema(tags=["Authentication - JWT Token"])
class CreateAuthTokenView(TokenObtainPairView):
    serializer_class = CreateJWTSerializer

    @extend_schema(
        request=CreateJWTSerializer,
        responses={200: {"description": "JWT tokens generated successfully."}},
        operation_id="Create JWT Token",
        description="Generate JWT tokens with optional OTP and profile data."
    )
    @track_activity(activity_type=ActivityType.LOGIN, async_mode=True, sensitive_fields=['identifier', 'password'])
    def post(self, request):
        logger.info("Auth token creation requested.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid login data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        identifier = data["identifier"]
        password = data["password"]
        send_otp = data.get("send_otp", False)
        with_profile = data.get("with_profile", False)

        user = User.objects.filter(
            Q(email=identifier.lower()) | Q(phone_number=identifier)
        ).only(
            'id', 'first_name', 'last_name', 'account_number', 'email',
            'phone_number', 'is_active', 'verified_email',
            'verified_phone_number', 'is_verified', 'is_loan_qualified', 'password'
        ).first()

        if not user:
            logger.warning("Login failed: user not found (%s)", identifier)
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            logger.warning("Login failed: invalid credentials for user %s", user.id)
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            logger.warning("Login failed: inactive user %s", user.id)
            return Response({"error": "User account is not active."}, status=status.HTTP_400_BAD_REQUEST)

        user_data = {}
        customer_profile_data = None

        if with_profile:
            user_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "account_number": user.account_number,
                "email": user.email,
                "phone_number": user.phone_number,
                "is_active": user.is_active,
                "is_email_verified": user.verified_email,
                "is_phone_verified": user.verified_phone_number,
                "is_verified": user.is_verified,
                "is_loan_qualified": user.is_loan_qualified,
            }

            customer_profile = CustomerProfileFormatter.get_optimized_queryset().filter(user=user).first()
            if customer_profile:
                customer_profile_data = CustomerProfileFormatter.prepare(customer_profile)

        if send_otp:
            otp = OTPManager.generate_otp(user.id)
            logger.info("OTP generated for user %s", user.id)

            if "@" in identifier:
                dispatch_email_verification_otp_task.delay(otp, user.email)
            else:
                dispatch_sms_verification_otp_task.delay(otp, user.phone_number)

        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data,
            "customerProfile": customer_profile_data,
        }

        return Response(tokens, status=status.HTTP_200_OK)


@extend_schema(tags=["Authentication - JWT Token"])
class RefreshAuthTokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    @extend_schema(
        request=RefreshTokenSerializer,
        responses={200: {"description": "JWT tokens refreshed successfully."}},
        operation_id="Refresh JWT Token",
        description="Refresh JWT tokens using a valid refresh token."
    )
    @track_activity(activity_type=ActivityType.LOGIN, async_mode=True)
    def post(self, request):
        logger.info("Token refresh requested.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid refresh token data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh"]

        try:
            refresh = RefreshToken(refresh_token)
            user = User.objects.get(id=refresh.payload.get("user_id"))

            new_tokens = {
                "refresh": str(RefreshToken.for_user(user)),
                "access": str(refresh.access_token),
            }

            logger.info("Token refreshed for user %s", user.id)
            return Response(new_tokens, status=status.HTTP_200_OK)

        except InvalidToken:
            logger.error("Invalid refresh token.")
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        except (User.DoesNotExist, KeyError) as e:
            logger.error("Refresh failed: %s", str(e))
            return Response({"error": f"Token validation error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication - JWT Token"])
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RevokeTokenSerializer

    @extend_schema(
        request=RevokeTokenSerializer,
        responses={
            205: {"description": "Successfully logged out."},
            400: {"description": "Invalid request or token."}
        },
        operation_id="Revoke JWT Token",
        description="Logout user by blacklisting their refresh token."
    )
    @track_activity(activity_type=ActivityType.LOGOUT, async_mode=True)
    def post(self, request):
        logger.info("Logout requested.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid logout data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = serializer.validated_data["refresh"]
            RefreshToken(refresh_token).blacklist()

            logger.info("User logged out.")
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except InvalidToken as e:
            logger.error("Invalid token during logout: %s", str(e))
            return Response({"error": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError as e:
            logger.error("Token error during logout: %s", str(e))
            return Response({"error": f"Token error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Unexpected error during logout.")
            return Response({"error": f"Failed to logout: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
