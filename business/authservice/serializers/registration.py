from rest_framework import serializers
from userservice.models import User


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    country_code = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'country_code', 'phone_number', 'password'
        ]


class RegisterVerificationSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    otp = serializers.CharField(max_length=6)


class ResendOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField()
