# userservice/serializers/user_serializers.py

from rest_framework import serializers

class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    currentPassword = serializers.CharField(write_only=True, min_length=6, max_length=6)


class ChangePhoneNumberSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    currentPassword = serializers.CharField(write_only=True, min_length=6, max_length=6)


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(write_only=True, min_length=6, max_length=6)
    newPassword = serializers.CharField(write_only=True, min_length=6, max_length=6)
    confirmPassword = serializers.CharField(write_only=True, min_length=6, max_length=6)

    def validate(self, data):
        if data['newPassword'] != data['confirmPassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class NotificationPreferenceSerializer(serializers.Serializer):
    use_sms = serializers.BooleanField(required=True)
