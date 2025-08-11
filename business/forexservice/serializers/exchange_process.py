from decimal import Decimal
from rest_framework import serializers
from .. import models as forex_models


class ExchangeRequestSerializer(serializers.ModelSerializer):
    source_currency = serializers.CharField(max_length=3)
    target_currency = serializers.CharField(max_length=3)
    source_amount = serializers.DecimalField(min_value=Decimal("0.00"), max_digits=10, decimal_places=2)

    class Meta:
        model = forex_models.RateSnapshot
        fields = ['source_currency', 'target_currency', 'source_amount']


class ExchangePreviewResponseSerializer(serializers.Serializer):
    source_currency = serializers.CharField()
    target_currency = serializers.CharField()
    source_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    platform_exchange_rate = serializers.DecimalField(max_digits=12, decimal_places=6)
    charged_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    converted_amount_with_fee = serializers.DecimalField(max_digits=12, decimal_places=2)


class ExchangeExecutionResponseSerializer(serializers.Serializer):
    source_currency = serializers.CharField()
    target_currency = serializers.CharField()
    source_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    base_exchange_rate = serializers.DecimalField(max_digits=12, decimal_places=6)
    platform_exchange_rate = serializers.DecimalField(max_digits=12, decimal_places=6)
    charged_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    converted_amount_with_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    reference_id = serializers.CharField()
    status = serializers.CharField()
    payment_provider = serializers.CharField()
