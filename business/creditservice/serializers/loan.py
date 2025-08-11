from rest_framework import serializers
from creditservice.models import Loan, Repayment
from userservice.serializers import UserProfilePublicSerializer


class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['amount']

    def validate_amount(self, value):
        user = self.context['request'].user
        if value > user.credit_profile.max_loan_amount:
            raise serializers.ValidationError(
                f"Amount exceeds maximum allowed ({user.credit_profile.max_loan_amount})"
            )
        return value

class LoanSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        source='get_balance',
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    user = UserProfilePublicSerializer(source='user.user', read_only=True)
    approved_by = UserProfilePublicSerializer(read_only=True)  # Removed source parameter
    repayments = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            'id', 'user', 'amount', 'status', 'reference_number',
            'disbursement_date', 'due_date', 'interest_accrued',
            'processing_fee', 'total_repayment', 'balance',
            'approved_by', 'approved_at', 'repayments'
        ]
        read_only_fields = [
            'status', 'disbursement_date', 'due_date',
            'interest_accrued', 'processing_fee', 'total_repayment'
        ]

    def get_repayments(self, obj):
        return RepaymentSerializer(
            obj.repayments.all(),
            many=True
        ).data
    

class LoanIDSerializer(serializers.Serializer):
    loan_id = serializers.UUIDField()

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = '__all__'
        read_only_fields = ['id', 'status', 'payment_date']
