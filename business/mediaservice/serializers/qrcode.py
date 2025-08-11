from rest_framework import serializers


class QRCodeEncryptRequestSerializer(serializers.Serializer):
    """Serializer for the data to be encrypted into a QR code."""
    data = serializers.DictField(help_text="Data to encrypt into QR code")


class QRCodeEncryptResponseSerializer(serializers.Serializer):
    """Serializer for the encrypted QR code response."""
    encrypted_data = serializers.CharField(help_text="Encrypted base64-encoded string")


class QRCodeDecryptRequestSerializer(serializers.Serializer):
    """Serializer for the encrypted QR code input."""
    data = serializers.CharField(help_text="Base64-encoded encrypted string")


class QRCodeDecryptResponseSerializer(serializers.Serializer):
    """Serializer for the decrypted QR code data."""
    decrypted_data = serializers.DictField(help_text="Decrypted original data")
