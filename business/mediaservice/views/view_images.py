from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes

from rbac.permissions import MethodPermission, register_permissions
from userservice.models import Customer


@register_permissions
@extend_schema(tags=["Media Services - Images"])
class CustomerImageView(APIView):
    """
    Endpoint to retrieve stored Customer image files.

    Supported image types: `front`, `back`, `face`, `address`.
    """

    permission_classes = [MethodPermission, AllowAny]

    # Method-specific permissions for implemented methods only
    get_permission = 'retrieve_customer_image'

    @extend_schema(
        request=None,
        responses={
            200: OpenApiTypes.BINARY,
            404: OpenApiTypes.STR,
        },
        operation_id="Retrieve Customer Image",
        description="Returns the requested Customer image file (JPEG) based on ID and image type.",
    )
    def get(self, request, id, image_type, *args, **kwargs):
        customer_record = get_object_or_404(Customer, id=id)

        image_data = {
            'front': customer_record.id_image_front,
            'back': customer_record.id_image_back,
            'face': customer_record.selfie_image,
            'address': customer_record.address_proof_image
        }.get(image_type)

        if not image_data:
            raise Http404("Image not found")

        return HttpResponse(image_data, content_type="image/jpeg")
