from decimal import Decimal
from rest_framework import serializers

class InitiateP2PTransferSerializer(serializers.Serializer):
    recipient_user = serializers.UUIDField(write_only=True)
    transfer_amount = serializers.DecimalField(
        write_only=True, min_value=Decimal("0.00"),
        decimal_places=2, max_digits=10
    )
    reason = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
