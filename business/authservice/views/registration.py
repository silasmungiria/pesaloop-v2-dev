import logging

# Third-party imports
from django.db import transaction as db_transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Project-specific imports
from walletservice.models import DigitalWallet, Currency
from userservice.models import User, Customer
from rbac.models import UserRole, Role
from authservice.serializers import RegisterSerializer
from authservice.services import OTPManager
from authservice.notifications import (
    dispatch_email_verification_otp_task,
    dispatch_wallet_creation_email_task,
)
from tracking.services import track_activity
from tracking.utils import ActivityType


logger = logging.getLogger(__name__)


@extend_schema(tags=["Authentication - User Registration"])
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        request=RegisterSerializer,
        responses={201: {"description": "User registered successfully."}},
        operation_id="Register User",
        description="Register a new user, create a wallet, and send OTP for email verification."
    )
    @track_activity(activity_type=ActivityType.AUTH, async_mode=True, sensitive_fields=['email', 'phone_number'])
    def post(self, request):
        logger.info("Received user registration request.")
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid registration data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")

        if email and User.objects.filter(email=email).exists():
            logger.warning("Registration failed: Email already exists - %s", email)
            return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=phone_number).exists():
            logger.warning("Registration failed: Phone number already exists - %s", phone_number)
            return Response({"error": "A user with this phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                user = User.objects.create_user(**validated_data)
                logger.info("Created new user: %s", user.id)

                otp = OTPManager.generate_otp(user.id)
                logger.info("Generated OTP for user %s", user.id)

                # Assign default role
                customer_role, _ = Role.objects.get_or_create(name="customer")
                UserRole.objects.create(user=user, role=customer_role)
                logger.info("Assigned 'customer' role to user %s", user.id)

                # Create customer profile
                Customer.objects.create(user=user)
                logger.info("Created customer profile for user %s", user.id)

                # Create wallet if email is provided
                if email:
                    currency, _ = Currency.objects.get_or_create(
                        code="KES", defaults={"name": "Kenyan Shilling"}
                    )
                    wallet = DigitalWallet.objects.create(
                        wallet_owner=user,
                        is_default=True,
                        currency=currency
                    )
                    logger.info("Created default wallet %s for user %s", wallet.id, user.id)

                    # Dispatch OTP and wallet creation emails after commit
                    db_transaction.on_commit(lambda: dispatch_email_verification_otp_task.delay(otp, user.email))
                    db_transaction.on_commit(lambda: dispatch_wallet_creation_email_task.delay(wallet.id, user.id))
                    logger.info("Dispatched OTP and wallet creation email tasks for user %s", user.id)

            return Response(
                {"message": "Registration successful. Verify using OTP sent to you."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.exception("Unexpected error during registration for email: %s", email)
            return Response(
                {"error": f"Registration failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
