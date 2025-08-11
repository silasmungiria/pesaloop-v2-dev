from rest_framework import serializers
from ..models import Employer

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['id', 'name', 'registration_number', 'is_verified', 'industry']

class EmployerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = [
            'name', 'registration_number', 'tax_id', 'industry',
            'annual_revenue', 'employee_count', 'address',
            'phone_number', 'email', 'website', 'bank_name',
            'bank_account', 'bank_branch', 'payroll_contact_name',
            'payroll_contact_email', 'payroll_contact_phone'
        ]
        extra_kwargs = {
            'registration_number': {'required': True},
            'tax_id': {'required': False}
        }


class EmployerVerificationSerializer(serializers.Serializer):
    employer_id = serializers.UUIDField()

