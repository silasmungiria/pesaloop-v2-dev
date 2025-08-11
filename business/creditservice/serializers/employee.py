from rest_framework import serializers
from ..models import CreditUser, Employer

class CreditUserSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.name', read_only=True)
    
    class Meta:
        model = CreditUser
        fields = [
            'id', 'user', 'employer', 'employer_name',
            'monthly_salary', 'verification_status',
            'verified_at'
        ]
        read_only_fields = ['verification_status', 'verified_at']


class UserVerificationInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    monthly_salary = serializers.DecimalField(max_digits=12, decimal_places=2)



class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    employer_code = serializers.CharField(write_only=True)
    
    class Meta:
        model = CreditUser
        fields = ['monthly_salary', 'employer_code']
        extra_kwargs = {
            'monthly_salary': {'required': True}
        }

    def validate(self, attrs):
        try:
            employer = Employer.objects.get(registration_number=attrs['employer_code'])
        except Employer.DoesNotExist:
            raise serializers.ValidationError("Invalid employer code")
        
        attrs['employer'] = employer
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('employer_code')
        return CreditUser.objects.create(
            user=user,
            **validated_data
        )
