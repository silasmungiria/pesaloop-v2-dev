from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from userservice.notifications import send_verification_email
from .image_compression import ImageCompressor
from .profile_formatter import CustomerProfileFormatter


class CustomerImageUploadHandler:
    @staticmethod
    def upload(request, serializer_class, image_type: str, success_message: str) -> Response:
        """
        Handle Customer image upload with compression, profile update, and notification dispatch.

        Args:
            request: DRF request with user and image data.
            serializer_class: Serializer for validating incoming image fields.
            image_type (str): One of ['face', 'front', 'back', 'address'].
            success_message (str): Message to return on success.

        Returns:
            Response: DRF Response with status and customer profile data or error.
        """

        customer_profile = CustomerProfileFormatter.get_optimized_queryset().filter(
            user=request.user
        ).first()

        if not customer_profile:
            return Response(
                {"message": "No Customer record found to update."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            with transaction.atomic():
                validated_data = serializer.validated_data

                # Compress uploaded images
                for field_name, file in validated_data.items():
                    if isinstance(file, (InMemoryUploadedFile, TemporaryUploadedFile)):
                        validated_data[field_name] = ImageCompressor.compress(file)

                # Update the profile with compressed image(s)
                serializer.update(customer_profile, validated_data)

                # Update upload flags
                image_upload_flags = {
                    "selfie": "is_face_uploaded",
                    "front": "is_id_front_uploaded",
                    "back": "is_id_back_uploaded",
                    "address": "is_address_proof_image_uploaded",
                }
                if image_type in image_upload_flags:
                    setattr(customer_profile, image_upload_flags[image_type], True)

                customer_profile.save()

                # Trigger status transition if all required documents are now present
                if (
                    not customer_profile.customer_verified
                    and customer_profile.verification_status == "partial_submission"
                    and all([
                        customer_profile.id_image_front,
                        customer_profile.id_image_back,
                        customer_profile.selfie_image,
                        customer_profile.address_proof_image,
                    ])
                ):
                    customer_profile.verification_status = "under_review"
                    customer_profile.remarks = "We are currently reviewing the documents you submitted."
                    customer_profile.save()

                    transaction.on_commit(lambda: send_verification_email.delay(
                        customer_profile.id,
                        verification_status=customer_profile.verification_status,
                    ))

                customer_profile_data = CustomerProfileFormatter.prepare(customer_profile)

            return Response(
                {"message": success_message, "customerProfile": customer_profile_data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
