from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """Serializer for user details."""
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()