from decimal import Decimal
from rest_framework import serializers
from paymentservice.models import TransactionRecord


class TopUpRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(min_value=Decimal("0.00"), max_digits=10, decimal_places=2)
    phone_number = serializers.CharField(max_length=15)
    metadata = serializers.JSONField(required=False)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Top-up amount must be greater than zero.")
        return value


class TopUpResponseSerializer(serializers.Serializer):
    reference_id = serializers.UUIDField()
    amount = serializers.DecimalField(min_value=Decimal("0.00"), max_digits=10, decimal_places=2)
    status = serializers.CharField()

    class Meta:
        model = TransactionRecord
        fields = ['reference_id', 'amount', 'status']

