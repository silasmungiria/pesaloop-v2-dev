import json
from cryptography.fernet import Fernet
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rbac.permissions import MethodPermission, register_permissions
from mediaservice.serializers import (
    QRCodeEncryptRequestSerializer,
    QRCodeEncryptResponseSerializer,
    QRCodeDecryptRequestSerializer,
    QRCodeDecryptResponseSerializer
)

ENCRYPTION_KEY = settings.PAYLOAD_ENCRYPTION_KEY


@register_permissions
@extend_schema(tags=["Media Services - QR Codes"])
class QRCodeEncryptDataView(APIView):
    """
    API endpoint to encrypt sensitive data for QR code usage.
    Returns an encrypted string that can be embedded in a QR code.
    """
    permission_classes = [IsAuthenticated, MethodPermission]
    serializer_class = QRCodeEncryptRequestSerializer
    response_serializer_class = QRCodeEncryptResponseSerializer

    # Method-specific permissions for implemented methods only
    post_permission = 'encrypt_qr_code_data'

    @extend_schema(
        request=serializer_class,
        responses={200: response_serializer_class},
        operation_id="Encrypt QR Code Data",
        description="Encrypts a JSON payload into a secure base64 string suitable for QR code use.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        fernet = Fernet(ENCRYPTION_KEY)
        try:
            data_to_encrypt = serializer.validated_data["data"]
            encrypted_data = fernet.encrypt(json.dumps(data_to_encrypt).encode()).decode("utf-8")
            return Response({"encrypted_data": encrypted_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Media Services - QR Codes"])
class QRCodeDecryptDataView(APIView):
    """
    API endpoint to decrypt a QR code payload.
    Accepts an encrypted base64 string and returns the original data.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = QRCodeDecryptRequestSerializer
    response_serializer_class = QRCodeDecryptResponseSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: response_serializer_class},
        operation_id="Decrypt QR Code Data",
        description="Decrypts a base64 string payload retrieved from a QR code into the original JSON data.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        fernet = Fernet(ENCRYPTION_KEY)
        try:
            encrypted_data = serializer.validated_data["data"]
            decrypted_data = fernet.decrypt(encrypted_data.encode()).decode("utf-8")
            return Response({"decrypted_data": json.loads(decrypted_data)}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or tampered QR Code"}, status=status.HTTP_400_BAD_REQUEST)
