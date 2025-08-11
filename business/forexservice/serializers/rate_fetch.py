from rest_framework import serializers
from .. import models as forex_models


class ExchangeRateSnapshotSerializer(serializers.ModelSerializer):
    """Serializer for triggering the exchange rates fetch."""
    class Meta:
        model = forex_models.RateSnapshot
        fields = ['id', 'response_data', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')