from rest_framework import serializers
from forexservice.models import CurrencyExchangeRecord
from .base import UserSerializer


class CurrencyExchangeSerializer(serializers.ModelSerializer):
    """Serializer for currency exchange records."""
    user = serializers.SerializerMethodField()
    is_debit = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyExchangeRecord
        fields = [
            'id', 'user', 'source_currency', 'target_currency', 'source_amount', 
            'platform_exchange_rate', 'converted_amount_with_fee', 'charged_amount', 
            'charged_amount_currency', 'payment_provider', 'metadata', 'reference_id', 'status', 'is_debit', 'transaction_type', 'created_at', 'updated_at'
        ]
        read_only_fields = fields

    def get_user(self, obj):
        """Return serialized user details."""
        return UserSerializer(obj.user).data
    
    def get_is_debit(self, obj):
        """Return True if the authenticated user initiated the exchange."""
        request = self.context.get('request')
        return request and request.user == obj.user