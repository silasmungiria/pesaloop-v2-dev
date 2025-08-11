# userservice/serializers/user_serializers.py
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from userservice.models import User


class UserProfilePublicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    verification_status = serializers.SerializerMethodField()
    
    @extend_schema_field(str)
    def get_full_name(self, obj) -> str:
        return obj.get_full_name()

    @extend_schema_field(str)
    def get_verification_status(self, obj) -> str:
        """Returns a string representation of verification status"""
        if obj.is_verified:
            return "fully_verified"
        elif obj.verified_email and obj.verified_phone_number:
            return "basic_verified"
        elif obj.verified_email or obj.verified_phone_number:
            return "partially_verified"
        return "not_verified"
    
    class Meta:
        model = User
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'full_name',
            'country_code',
            'verification_status',
            'date_joined'
        ]
        read_only_fields = fields

class UserProfileStandardSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    verification_status = serializers.SerializerMethodField()
    
    @extend_schema_field(str)
    def get_full_name(self, obj) -> str:
        return obj.get_full_name()

    @extend_schema_field(str)
    def get_verification_status(self, obj) -> str:
        """Returns a string representation of verification status"""
        if obj.is_verified:
            return "fully_verified"
        elif obj.verified_email and obj.verified_phone_number:
            return "basic_verified"
        elif obj.verified_email or obj.verified_phone_number:
            return "partially_verified"
        return "not_verified"
    
    class Meta:
        model = User
        fields = [
            'id',
            'account_number',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'country_code',
            'verified_email',
            'verified_phone_number',
            'is_active',
            'is_verified',
            'verification_status',
            'date_joined'
        ]
