# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.models import Customer
from userservice.serializers import CustomerDocInfoSerializer
from userservice.services import CustomerProfileFormatter


@register_permissions
@extend_schema(tags=["User Services - KYC"])
class CustomerFormSubmissionView(APIView):
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = CustomerDocInfoSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'submit_kyc_verification_form'

    @extend_schema(
        request=serializer_class,
        responses={201: {
            "message": "Customer verification submitted successfully.",
            "customerProfile": "CustomerProfileData"
            }
        },
        operation_id="Submit KYC Verification Form",
        description="Endpoint for users to submit their Customer verification details."
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        customer_profile = CustomerProfileFormatter.get_optimized_queryset().filter(
            user=user
        ).first()

        if customer_profile:
            if customer_profile.customer_verified and customer_profile.verification_status == 'verified':
                return Response({"error": "Customer already verified."}, status=status.HTTP_400_BAD_REQUEST)

            if customer_profile.verification_status == 'under_review':
                return Response({"error": "Customer verification already in review."}, status=status.HTTP_400_BAD_REQUEST)

            customer_profile.verification_status = 'partial_submission'
            customer_profile.save()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            new_customer_profile = Customer.objects.create(user=user, **validated_data)
            customer_profile_data = CustomerProfileFormatter.prepare(new_customer_profile)
            return Response(
                {"message": "Customer verification submitted successfully.", "customerProfile": customer_profile_data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
