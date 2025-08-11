from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.db.models import Q

from userservice.models import User


@extend_schema(tags=["Integration - Mpesa C2B"])
class C2BValidationView(APIView):
    """
    Validates C2B Paybill payments by checking if the provided BillRefNumber 
    matches an existing user account number, phone number, or email.
    """
    permission_classes = [AllowAny]

    # {    
    # "ResultCode": "C2B00011",
    # "ResultDesc": "Rejected",
    # }

    @extend_schema(
        request=None,
        responses=None,
        operation_id="C2B User Validate",
        description="Endpoint for validating C2B Paybill payments by checking user account details."
    )
    def post(self, request, *args, **kwargs):
        callback_data = request.data
        bill_ref_number = callback_data.get("BillRefNumber")

        if not bill_ref_number or not bill_ref_number.strip():
            return Response({"ResultCode": "C2B00012", "ResultDesc": "Invalid Account Number"})

        try:
            user = User.objects.filter(
                Q(phone_number=bill_ref_number) |
                Q(email=bill_ref_number) |
                Q(account_number=bill_ref_number)
            ).first()

            if not user:
                return Response({"ResultCode": "C2B00014", "ResultDesc": "User not found"})

            return Response({"ResultCode": "0", "ResultDesc": "Accepted"})

        except Exception:
            return Response({"ResultCode": "C2B00016", "ResultDesc": "Other Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
