from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)
