# Third-party imports
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Project-specific imports
from rbac.permissions import MethodPermission, register_permissions
from userservice.serializers import (
    CustomerProofAddressSerializer,
    CustomerIDBackSerializer,
    CustomerSelfieSerializer,
    CustomerIDFrontSerializer,
    CustomerImageBaseSerializer,
)
from userservice.services import CustomerImageUploadHandler


@register_permissions
@extend_schema(tags=["User Services - KYC"])
class CustomerImageUploadView(GenericAPIView):
    permission_classes = [IsAuthenticated, MethodPermission]

    # Method-specific permissions for implemented methods only
    put_permission = 'upload_customer_image'

    serializer_mapping = {
        "address": CustomerProofAddressSerializer,
        "back": CustomerIDBackSerializer,
        "selfie": CustomerSelfieSerializer,
        "front": CustomerIDFrontSerializer,
    }

    def get_serializer_class(self):
        image_type = self.kwargs.get("image_type")
        return self.serializer_mapping.get(image_type)

    @extend_schema(
        request=CustomerImageBaseSerializer,
        responses={200: {"message": "Image uploaded successfully."}},
        operation_id="Upload Customer Image",
        description="Endpoint for users to upload a specific type of customer image. Allowed types: 'face', 'front', 'back', 'address'.",
    )
    def put(self, request, *args, **kwargs):
        image_type = kwargs.get("image_type")
        serializer_class = self.get_serializer_class()

        if not serializer_class:
            return Response(
                {"error": f"Invalid image type '{image_type}'. Must be one of: {list(self.serializer_mapping.keys())}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return CustomerImageUploadHandler.upload(
            request=request,
            serializer_class=serializer_class,
            image_type=image_type,
            success_message=f"{image_type.capitalize()} image uploaded successfully.",
        )
