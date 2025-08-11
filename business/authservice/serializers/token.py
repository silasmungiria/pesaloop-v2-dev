from rest_framework import serializers


class CreateJWTSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    send_otp = serializers.BooleanField(default=False)
    with_profile = serializers.BooleanField(default=False)


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


class RevokeTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
