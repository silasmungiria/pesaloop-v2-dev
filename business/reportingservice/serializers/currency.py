from rest_framework import serializers
from walletservice import models as wallet_models


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for currency details."""
    
    class Meta:
        model = wallet_models.Currency
        fields = ['code', 'name']
        read_only_fields = fields