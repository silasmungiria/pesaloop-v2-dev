# Third-party imports
from django.db import transaction as db_transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.models import User
from paymentservice.serializers import RecipientVerificationSerializer


@register_permissions
@extend_schema(tags=["Payment Service - Recipient"])
class VerifyRecipientView(APIView):
    """
    Retrieves recipient account details (email or phone) for P2P transfers.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = RecipientVerificationSerializer

    # Method-specific permissions for implemented methods only
    get_permission = 'verify_recipient'

    @extend_schema(
        request=None,
        responses=serializer_class,
        operation_id="Verify Recipient",
        description="Endpoint for verifying recipient details using email or phone number."
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieves recipient details using email or phone.
        
        Query Parameters:
            - `email` (str): Recipient's email.
            - `phone` (str): Recipient's phone number.

        Returns:
            Response: Recipient details or error message.
        """
        recipient_email = request.query_params.get('email')
        recipient_phone = request.query_params.get('phone')

        if not recipient_email and not recipient_phone:
            return Response({"error": "Either 'email' or 'phone' query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                recipient_user = User.objects.select_for_update().get(email=recipient_email) if recipient_email else User.objects.select_for_update().get(phone_number=recipient_phone)

                if not recipient_user:
                    return Response({"error": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)
                
                if recipient_user == request.user:
                    return Response({"error": "You cannot send money to yourself."}, status=status.HTTP_400_BAD_REQUEST)

                recipient_serializer = self.serializer_class(recipient_user)
                return Response(recipient_serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
