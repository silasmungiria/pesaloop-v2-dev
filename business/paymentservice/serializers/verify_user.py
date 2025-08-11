from rest_framework import serializers
from userservice import models as user_models

class RecipientVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'is_active', 'is_verified']
        read_only_fields = fields
